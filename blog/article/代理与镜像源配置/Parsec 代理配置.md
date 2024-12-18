# Parsec 代理配置

Windows 平台上配置文件路径如下:  
* 用户安装: `%appdata%\Parsec\config.txt`
* 系统安装: `%ProgramData%\Parsec\config.txt`

在配置文件中写入代理配置:  

```
app_proxy = true
app_proxy_scheme = http
app_proxy_address = localhost
app_proxy_port = 7890
```