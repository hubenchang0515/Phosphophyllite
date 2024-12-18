# Ubuntu CUDA 驱动升级失败的问题

升级时失败

```
sudo apt update
sudo apt upgrade
```

错误信息：  

```
$ sudo apt --fix-broken install
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Correcting dependencies... Done
The following package was automatically installed and is no longer required:
  nvidia-firmware-535-535.129.03
Use 'sudo apt autoremove' to remove it.
The following additional packages will be installed:
  nvidia-kernel-common-535
The following packages will be upgraded:
  nvidia-kernel-common-535
1 upgraded, 0 newly installed, 0 to remove and 32 not upgraded.
1 not fully installed or removed.
Need to get 0 B/38,3 MB of archives.
After this operation, 61,2 MB of additional disk space will be used.
Do you want to continue? [Y/n] y
(Reading database ... 291692 files and directories currently installed.)
Preparing to unpack .../nvidia-kernel-common-535_535.129.03-0ubuntu1_amd64.deb .
..
Unpacking nvidia-kernel-common-535 (535.129.03-0ubuntu1) over (535.129.03-0ubunt
u0.22.04.1) ...
dpkg: error processing archive /var/cache/apt/archives/nvidia-kernel-common-535_
535.129.03-0ubuntu1_amd64.deb (--unpack):
 trying to overwrite '/lib/firmware/nvidia/535.129.03/gsp_ga10x.bin', which is a
lso in package nvidia-firmware-535-535.129.03 535.129.03-0ubuntu0.22.04.1
dpkg-deb: error: paste subprocess was killed by signal (Broken pipe)
Errors were encountered while processing:
 /var/cache/apt/archives/nvidia-kernel-common-535_535.129.03-0ubuntu1_amd64.deb
E: Sub-process /usr/bin/dpkg returned an error code (1)
```

从错误信息上看，应该是 `nvidia-kernel-common-535` 和 `nvidia-firmware-535-535.129.03` 两个包
都包含了 `/lib/firmware/nvidia/535.129.03/gsp_ga10x.bin` 这个文件。

解决办法：  

只需要指定使用其中一个包的该文件即可

```
sudo dpkg -i --force-overwrite /var/cache/apt/archives/nvidia-kernel-common-535_535.129.03-0ubuntu1_amd64.deb
```