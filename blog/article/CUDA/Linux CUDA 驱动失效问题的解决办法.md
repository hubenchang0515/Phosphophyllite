# Linux CUDA 驱动失效问题的解决办法

在使用 Linux 的时候，如果经常进行升级，时不时会遇到驱动失效的问题:  

```
$ nvidia-smi 
NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver. 
Make sure that the latest NVIDIA driver is installed and running.
```

这是由于升级后 NVIDIA 驱动版本与内核或显卡不匹配的导致的。

首先通过 `uname` 命令查看当前内核版本，可以看到这里为 `6.5.0-35-generic`:  

```
$ uname -a
Linux ROG 6.5.0-35-generic #35~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Tue May  7 09:00:52 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
```

然后通过查看当前使用的 NVIDIA 驱动版本，可以看到这里为 `555.42.02`:  
```
$ ls /usr/src/ | grep nvidia
nvidia-555.42.02
```

通过[官网](https://www.nvidia.cn/Download/index.aspx)搜索可用的驱动版本，这里可以看到最新可用版本是 `550.90.07`:  

![搜索](https://raw.githubusercontent.com/hubenchang0515/resource/master/nvidia-driver/search.png)

![版本](https://raw.githubusercontent.com/hubenchang0515/resource/master/nvidia-driver/version.png)


安装对应版本的驱动:  

```
sudo apt install nvidia-driver-550
sudo dkms install -m nvidia -v 550.90.07
```

> **注意**  
> 如果开启了 UEFI Secure Boot，在安装驱动时会请求输入一段密钥。  
> 重启后会进入一个特殊的页面，需要在该页面上选择登记密钥（enroll key）输入相同的密钥，然后驱动才能访问固件。  