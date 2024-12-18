# 通过 systemd service 控制 x11vnc

创建 `/usr/lib/systemd/user/x11vnc.service` 文件，写入以下内容:  
```ini
[Unit]
Description=X11 VNC Server
Requires=graphical-session.target
After=graphical-session.target

[Service]
Type=simple
ExecStart=/usr/bin/x11vnc -forever
ExecStop=/usr/bin/x11vnc -R stop
Restart=on-failure
RestartSec=2

[Install]
WantedBy=multi-user.target
```

执行 `systemctl --user daemon-reload` 命令，刷新服务。

操作命令:  

* 启动 `systemctl --user start x11vnc`
* 停止 `systemctl --user stop x11vnc`
* 启用开机自启 `systemctl --user enable x11vnc`
* 停用开机自启 `systemctl --user disable x11vnc`