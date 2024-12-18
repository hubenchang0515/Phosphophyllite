# 使用 Docker 配置交叉编译环境

1. 首先 [安装 Docker](https://gist.github.com/hubenchang0515/8106a35156248a0654e8f52615e00bd0#%E5%AE%89%E8%A3%85-docker)
2. 然后下载 ubuntu 作为基础镜像 `sudo docker pull ubuntu:20.04`
3. 启动容器 `sudo docker run -h aarch64 --name aarch64 -it ubuntu:20.04`

> 最新版 ubuntu 22.04 的 `libc6-dev-arm64-cross` 为 2.35，与目标平台上的版本 2.28 不兼容，因此使用 20.04 版本的镜像。

## 安装交叉工具链

```
apt update
apt install gcc-aarch64-linux-gnu g++-aarch64-linux-gnu
```

> 编译裸机(bare-metal)程序时需要使用 aarch64-none-elf 版本的工具链，可以从 [ARM官网](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads) 下载。

## 编译 Qt

安装依赖:  

```
apt install build-essential python3 python-is-python3 perl ruby wget xz-utils
```

从 Qt 官网的主页进入下载页面需要填写姓名、公司、邮箱、电话等信息，很麻烦。
可以直接从 [download.qt.io](https://download.qt.io/official_releases/qt/5.15/5.15.8/) 页面下载源码。

```
wget https://download.qt.io/official_releases/qt/5.15/5.15.8/single/qt-everywhere-opensource-src-5.15.8.tar.xz
tar xvf qt-everywhere-opensource-src-5.15.8.tar.xz
cd qt-everywhere-opensource-src-5.15.8
./configure -opensource -confirm-license -release -xplatform linux-aarch64-gnu-g++ -no-opengl
make
make install
```

## 配置交叉编译环境

如果该环境只用于进行交叉编译，为了方便使用，可以将 gcc 等符号链接到 aarch64-linux-gnu-gcc 上:  

```bash
#! /usr/bin/bash

PREFIX="/usr/bin"
PLATFORM="aarch64-linux-gnu"

TOOLS=$(ls $PREFIX/$PLATFORM-*)

for TOOL in $TOOLS
do
        NAME=${TOOL##*$PLATFORM-}
        update-alternatives --install /usr/bin/$NAME $NAME $TOOL 100
done

# cc 和 cxx
update-alternatives --install $PREFIX/cc cc  $PREFIX/$PLATFORM-gcc 100
update-alternatives --install $PREFIX/cxx cxx $PREFIX/$PLATFORM-g++ 100
```

## 导出镜像

```
sudo docker commit 8cae637c3cc0 aarch64-cross-platform
sudo docker save -o aarch64-cross-platform.tar aarch64-cross-platform
```


## 遇到的问题

### libc 版本不匹配

将编译生成的可执行文件拷贝到目标设备上运行，报错:  

```
/usr/lib/libc.so.6: version GLIBC_2.34 not found (required by demo)
```

目标设备上的 libc 运行时版本为 2.28，而交叉编译环境上的版本为 2.35:  

```
apt policy libc6-dev-arm64-cross
libc6-dev-arm64-cross:
  Installed: 2.35-0ubuntu1cross3
  Candidate: 2.35-0ubuntu1cross3
  Version table:
 *** 2.35-0ubuntu1cross3 500
        500 https://mirrors.tuna.tsinghua.edu.cn/ubuntu jammy/main amd64 Packages
        100 /var/lib/dpkg/status
```

从 [Ubuntu Packages](https://packages.ubuntu.com/) 或 [Debian Packages](https://www.debian.org/distrib/packages) 下载对应版本的 deb 包并安装:

> 由于 Ubuntu Packages 上没有 2.28 版本的包，因此从 Debian Packages 上下载。  
> `libc6-arm64-cross_2.28-7cross1_all.deb` 是 `libc6-dev-arm64-cross_2.28-7cross1_all.deb` 的依赖项。  

```
wget http://ftp.cn.debian.org/debian/pool/main/c/cross-toolchain-base/libc6-dev-arm64-cross_2.28-7cross1_all.deb
wget http://ftp.cn.debian.org/debian/pool/main/c/cross-toolchain-base/libc6-arm64-cross_2.28-7cross1_all.deb
dpkg -i libc6-arm64-cross_2.28-7cross1_all.deb libc6-dev-arm64-cross_2.28-7cross1_all.deb
```

* 这样降级后，可以正常编译 C 语言程序，但是 `libstdc++` 依赖 `libc`，无法编译 C++ 程序。因此建议使用低版本的操作系统镜像。

### 编译 Qt 时的一些问题

`./configure -opensource -confirm-license -release` 产生错误 `qmake: cannot execute binary file: Exec format error`

因为编译 Qt 时需要编译生成 qmake，如果将 gcc 等软链接到了 aarch64-linux-gnu- 上，那么遍出来的 qmake 是 aarch64 架构的，无法在宿主机上运行。

需要将软链接改回 x86_64 架构:  

```
root@aarch64 # update-alternatives --config cxx
There are 4 choices for the alternative cxx (providing /usr/bin/cxx).

  Selection    Path                               Priority   Status
------------------------------------------------------------
  0            /usr/bin/aarch64-linux-gnu-g++      100       auto mode
* 1            /usr/bin/aarch64-linux-gnu-g++      100       manual mode
  2            /usr/bin/aarch64-linux-gnu-g++-11   100       manual mode
  3            /usr/bin/g++-11                     80        manual mode
  4            /usr/bin/x86_64-linux-gnu-g++       100       manual mode

Press <enter> to keep the current choice[*], or type selection number: 4
update-alternatives: using /usr/bin/x86_64-linux-gnu-g++ to provide /usr/bin/cxx (cxx) in manual mode

```

然后通过 `-xplatform` 选择交叉工具链进行编译:  

```
./configure -opensource -confirm-license -release -xplatform linux-aarch64-gnu-g++ -no-opengl
make
```

> `-xplatform` 的可选项在 `qtbase/mkspecs` 目录里查看


* `ERROR: The OpenGL functionality tests failed!` 的问题可以通过添加 `-no-opengl` 解决，也可以安装对应架构的 `libgl1-mesa-dev` 包。
* `ERROR: Python is required to build QtQml.` 的问题，可以通过安装 `python-is-python3` 解决。再次运行 `./configure` 需要添加 `-recheck-all` 重新检查依赖。
* `BEGIN failed--compilation aborted at ..../generate.pl line 35.` 的问题可以通过安装新版本的 `perl` 解决。
* `error: 'mimetype_database' was not declared in this scope` 的问题可以通过安装新版本 `perl`, `ruby` 和 `python` 解决。