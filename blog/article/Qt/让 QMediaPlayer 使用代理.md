# 让 QMediaPlayer 使用代理


## QMediaPlayer 使用简介
使用 `QMediaPlayer::setSource` 设置媒体源，即可进行播放：  

```cpp
player = new QMediaPlayer;
audioOutput = new QAudioOutput;
player->setAudioOutput(audioOutput);
connect(player, &QMediaPlayer::positionChanged, this, &MediaExample::positionChanged);
player->setSource(QUrl("https://vjs.zencdn.net/v/oceans.mp4"));
audioOutput->setVolume(50);
player->play();
```

> 上述代码使用 Qt6，Qt6 对 Multimedia 模块做了较大改动，与 Qt5 不兼容。


## 问题描述

`QMediaPlayer` 在播放网络源时，会预先加载一段时间，然后开始播放，预先加载的部分是流畅的，但如果网速慢于播放速度后续就会产生卡顿。

上述示例中使用的视频源来自 [video.js](https://github.com/videojs/video.js)，播放时卡顿非常严重，经分析应是网速太慢导致的。

## 应用代理无效

通过 `QNetworkProxy::setApplicationProxy` 可以设置应用程序的全局代理，相应的 `QNetworkProxy::applicationProxy` 可以查看应用程序的全局代理。

> 当系统设置了代理是，Qt 会自动设置应用代理，通过 `QNetworkProxy::applicationProxy` 查看即可可以确认这一点，不需要手动设置。

但经过测试，`QMediaPlayer` 完全无视了应用代理，仍然卡顿。

## 解决办法

### 手动使用 QtNetwork 设置代理并请求数据源

可以手动使用 `QNetworkAccessManager` 请求网络源，并将返回的 `QNetworkReply` 设为 `QMediaPlayer` 的源：  

```cpp
manager = new QNetworkAccessManager;
manager.setProxy(QNetworkProxy()); // QNetworkAccessManager 会使用应用代理，这行可省略
reply = manager->get(QNetworkRequest(QUrl("https://vjs.zencdn.net/v/oceans.mp4")));

player->setSourceDevice(reply);
player->play();
```

### 预加载

上述示例并不能直接运行，因为返回时 `QNetworkReply` 还没有拿到数据。而 `QMediaPlayer` 不支持阻塞式读取。

因此需要等待 `QNetworkReply` 预加载一部分数据后再将其设为 `QMediaPlayer` 的数据源。

```cpp
#define PRELOAD_SIZE 1024 * 1024

manager = new QNetworkAccessManager;
manager.setProxy(QNetworkProxy()); // QNetworkAccessManager 会使用应用代理，这行可省略
reply = manager->get(QNetworkRequest(QUrl("https://vjs.zencdn.net/v/oceans.mp4")));

// 等待 readyRead 并检查数据长度，达到一定的数据量时开始播放
connect(reply, &QNetworkReply::readyRead, [reply, player](){
    if (reply->size() >= PRELOAD_SIZE)
    {
        player->setSourceDevice(reply);
        player->play();
        disconnect(reply, &QNetworkReply::readyRead); // 断开与 readyRead 信号连接的所有槽
    }
});

// 如果媒体源非常小，总数据两都小于 PRELOAD_SIZE，则在 finished 触发时开始播放
connect(reply, &QNetworkReply::finished, [reply, player](){
    if (reply->size() >= PRELOAD_SIZE)
    {
        player->setSourceDevice(reply);
        player->play();
        disconnect(reply, &QNetworkReply::finished); // 断开与 finished 信号连接的所有槽
    }
});
```

### 流媒体

对于 m3u8 之类的流媒体，实际数据被切分为多个文件，m3u8 仅仅是文件索引。

使用 `QNetworkAccessManager` 发起请求时，仅仅获得了索引文件本身，需要手动解析并请求后续内容。