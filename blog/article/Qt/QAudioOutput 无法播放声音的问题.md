# QAudioOutput 无法播放声音的问题

在 Windows 上使用 MSVC 编译的 Qt 程序，无法播放声音，`QAudioDeviceInfo::availableDevices` 返回空列表。

这是因为没能正确加载 Qt 插件。需要将 `Qt\msvc2017_64\plugins` 目录下的 audio 目录复制到可执行文件所在目录。

使用 `windeployqt` 部署后即可正确运行。

插件加载正确后，仍然发生无声音的问题，且 Qt 无任何报错。通过 QAudioDeviceInfo 查看支持的音频格式为：

```
("audio/pcm")
(8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 192000)
(8, 16, 24, 32, 48, 64)
(LittleEndian)
(SignedInt, UnSignedInt, Float)
```

程序设置的音频格式为 **32 位、小端、浮点数**，在支持的范围内。

[这个问题](https://stackoverflow.com/questions/15594180/qaudiooutput-in-qt5-is-not-producing-any-sound)上的回答提到:  

> Qt 音频在 Windows 上，8 位数据只支持 UnSignedInt，16 位数据支持 SignedInt

但是没有提到 float 类型，怀疑可能不支持，改用 16 位 SignedInt 后可以正常播放。

> 另外，使用其支持列表返回的 64 位会报错，可以判断支持列表是假的。