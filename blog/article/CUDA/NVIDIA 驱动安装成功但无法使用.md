# NVIDIA驱动安装成功但无法使用

## 现象

```
$ nvidia-smi
NVIDIA-SMI has failed because it couldn’t communicate with the NVIDIA driver. Make sure that the latest NVIDIA driver is installed and running.

$ dkms status
nvidia, 470.86, 5.13.0-22-generic, x86_64: installed

$ nvidia-settings:

ERROR: NVIDIA driver is not loaded
ERROR: Unable to load info from any available system
```

## 原因与解决办法

如果开启了 UEFI Secure Boot，在安装驱动时会请求输入一段密钥。  
重启后会进入一个特殊的页面，需要在该页面上选择登记密钥（enroll key）输入相同的密钥，然后驱动才能访问固件。  

> 也可以从 BIOS 上关闭 Secure Boot