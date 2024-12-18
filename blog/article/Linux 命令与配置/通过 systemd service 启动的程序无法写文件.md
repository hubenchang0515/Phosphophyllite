# 通过systemd service启动的程序无法写文件

编译安装 [NetworkManager](https://gitlab.freedesktop.org/NetworkManager/NetworkManager) 之后，网络功能瘫痪。提示 `read-only file system`:  

```
$ nmcli device wifi rescan
$ nmcli device wifi connect HBC-WiFi
Error: Failed to add/activate new connection: failure adding connection: 
error writing to file '/usr/etc/NetworkManager/system-connections/HBC-WiFi.nmconnection': 
failed to create file /usr/etc/NetworkManager/system-connections/HBC-WiFi.nmconnection.QZNRI1:read-only file system
```

但是直接使用命令启动 NetworkManager 时没有这个现象，命令可以正常执行。

```
sudo NetworkManager --no-daemon
```

原因是 `NetworkManager.service` 中的配置包含 `ProtectSystem=true`。此配置项使进程以只读模式挂载 `/usr` 与 `/boot` 目录。参考: [systemd.exec](https://www.freedesktop.org/software/systemd/man/systemd.exec.html#ProtectSystem=)

导致这个问题的原因是编译 NetworkManager 时，设置了 `--prefix=/usr`。正确的配置应该是 `--prefix=/`。