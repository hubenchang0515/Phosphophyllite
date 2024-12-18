# APT 更新时忽略指定的包

> 因为网络原因，系统升级时遇到某个包下载失败导致系统无法升级

保持包版本不更新:  

```
sudo apt-mark hold <package>
```

取消保持包版本:

```
sudo apt-mark unhold <package>
```