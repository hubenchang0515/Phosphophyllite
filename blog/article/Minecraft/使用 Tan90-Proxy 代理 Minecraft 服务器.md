# 使用 Tan90-Proxy 代理 Minecraft 服务器

[Tan90-Proxy](https://github.com/hubenchang0515/Tan90-Proxy) 是一个 NAT 穿透代理服务器。

可以将 Minecraft 服务程序部署在本地，然后通过一个廉价低配的公网服务器转发，从而降低开服成本。

一些服务器优惠页面:  

* [腾讯云优惠主机](https://curl.qcloud.com/G7jGsYZL)
* [阿里云优惠主机](https://www.aliyun.com/minisite/goods?userCode=gtmsv57a)
* [野草云海外主机](https://my.yecaoyun.com/aff.php?aff=5087)

> 因为公网服务器仅负责转发网络请求，同价位下建议购买带宽更高的产品。

Minecraft 服务程序下载页地址:  

* Java 版 - https://www.minecraft.net/zh-hans/download/server
* 基岩版 - https://www.minecraft.net/zh-hans/download/server/bedrock

## 代理服务器配置

在代理服务器上编辑配置文件 `server.ini`:  

```ini
[Proxy of Minecraft]
true_client_ip = 0.0.0.0                # 玩家连接这个 IP 地址，0.0.0.0 表示本机的所有 IP 地址
true_client_port = 25565                # 玩家连接这个端口
proxy_client_ip = 0.0.0.0               # 代理客户端连接这个 IP 地址，0.0.0.0 表示本机的所有 IP 地址
proxy_client_port = 8103                # 代理客户端连接这个端口
```

运行 `tan90-server`，出现此日志表面正常启动:  

```
[INFO]    : Config Proxy (Proxy of Minecraft) 0.0.0.0:25565 ----- 0.0.0.0:8103
```

## 代理客户端配置

启动 Minecraft 服务程序:  

```bash
java -Xmx1024M -Xms1024M -jar server.jar nogui
```

![启动 Minecraft 服务程序](https://github.com/hubenchang0515/resource/blob/master/tan90-proxy/pic-01.png?raw=true)

```ini
[Proxy of Minecraft]
proxy_server_ip = 68.68.98.53           # 代理服务器的 IP 地址，根据实际情况配置
proxy_server_port = 8103                # 代理服务器的端口，需要和上面的 proxy_client_port 一致
true_server_ip = localhost              # 实际的 Minecrafe 服务器 IP 地址，根据实际情况配置，localhost 是本机
true_server_port = 25565                # 实际的 Minecrafe 服务器的端口，根据实际情况配置，25565 是默认端口
```

运行 `tan90-client`，出现此日志表面正常启动并成功连接代理服务器:  

```
[INFO]    : Config Proxy (Proxy of Minecraft) 68.68.98.53:8103 ----- 0.0.0.0:25565
[INFO]    : Connected control connection to 68.68.98.53:8103 by 68.68.98.53:63654.
```

同时，服务端会显示此日志:  

```
[INFO]    : Get control connection from xxx.xxx.xxx.xxx:xxxxx.
```

## 启动游戏

在编辑服务器信息时，服务器地址填 `true_client_ip`:`true_client_port`:  

![填写服务器](https://github.com/hubenchang0515/resource/blob/master/tan90-proxy/pic-02.png?raw=true)

尝试进入游戏:  

![服务器列表](https://github.com/hubenchang0515/resource/blob/master/tan90-proxy/pic-03.png?raw=true)

![进入游戏](https://github.com/hubenchang0515/resource/blob/master/tan90-proxy/pic-04.png?raw=true)