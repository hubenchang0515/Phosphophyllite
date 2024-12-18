## Systemd 服务的代理配置

以 Docker 为例，创建或编辑 `/etc/systemd/system/docker.service.d/http-proxy.conf` 文件，写入以下内容:  

```conf
[Service]
Environment="ALL_PROXY=http://192.168.1.100:7890"
Environment="HTTP_PROXY=http://192.168.1.100:7890"
Environment="HTTPS_PROXY=http://192.168.1.100:7890"
```

然后重启:  

```
sudo systemctl daemon-reload
sudo systemctl restart docker
```