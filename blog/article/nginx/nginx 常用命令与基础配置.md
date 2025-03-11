# nginx 常用命令与基础配置

## 常用命令  

1. 启动: `nginx`
2. 使用指定配置文件启动: `nginx -c /path/to/file`
3. 正常停止: `nginx -s quit`
4. 快速停止: `nginx -s stop`
5. 重新加载配置: `nginx -s reload` 或 `systemctl reload nginx`
6. 重启: `systemctl restart nginx`
7. 测试配置文件: `nginx -t`

## 基础配置

> nginx 的默认配置文件路径为 `/etc/nginx/nginx.conf`
> 该文件初始包含了 `include /etc/nginx/conf.d/*.conf;` 和 `include /etc/nginx/sites-enabled/*;`
> 通常将自定义的配置文件写到 `/etc/nginx/sites-available/` 目录中，然后软链接到 `/etc/nginx/sites-enabled/`

基础示例:  

```nginx
server {
    listen       80;                  # 监听的端口
    server_name  localhost;           # 服务器名称或域名
 
    location / {
        root   /usr/share/nginx/html; # 网站根目录
        index  index.html index.htm;   # 默认页面
    }
}
```

通过反向代理绕过 CORS:  

```nginx
server {
    listen       80;
    server_name  localhost;
 
    location / {
        proxy_hide_header Access-Control-Allow-Origin;
        proxy_hide_header Access-Control-Allow-Headers;
        proxy_hide_header Access-Control-Allow-Methods;
        add_header Access-Control-Allow-Origin '*' always;
        add_header Access-Control-Allow-Headers '*' always;
        add_header Access-Control-Allow-Methods '*' always;
        proxy_ssl_server_name on;
        proxy_pass $URL; 
    }
}
```

代理尝试多个后端:  

```nginx
http {
    upstream backend {
        # 定义多个后端服务器
        server backend1.example.com;  # 第一个后端服务器
        server backend2.example.com;  # 第二个后端服务器
        server backend3.example.com;  # 第三个后端服务器

        # 可以添加更多的后端服务器
    }

    server {
        listen 80;  # 监听端口

        location / {
            proxy_pass http://backend;  # 将请求代理到 upstream 定义的后端服务器
            proxy_set_header Host $host;  # 设置 Host 头
            proxy_set_header X-Real-IP $remote_addr;  # 设置真实 IP
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;  # 设置 X-Forwarded-For 头
            proxy_set_header X-Forwarded-Proto $scheme;  # 设置协议头
        }

        # 可选：设置错误页面或超时
        error_page 502 = @fallback;  # 如果所有后端都不可用，跳转到 fallback
    }

    location @fallback {
        # 处理所有后端都不可用的情况
        return 503 "Service Unavailable";  # 返回 503 状态码
    }
}
```