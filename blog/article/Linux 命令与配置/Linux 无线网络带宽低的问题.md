# Linux 无线网络带宽低的问题

将 `/etc/modprobe.d/iwlwifi.conf` 文件中的 `11n_disable=1` 改为 `11n_disable=0`，然后重启系统。