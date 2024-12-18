# APT 代理配置

最近遇到 APT 连不上 docker 源的问题，需要配置 APT 的代理。  

创建 `/etc/apt/apt.conf.d/50proxy.conf` 文件，填入代理配置:  

```
Acquire::http::Proxy "http://ADDRESS:PORT";
```