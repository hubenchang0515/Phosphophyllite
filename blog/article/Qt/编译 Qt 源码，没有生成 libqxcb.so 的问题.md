# 编译 Qt 源码，没有生成 libqxcb.so 的问题

Qt 通过不同的插件，在不同的平台上进行显示，例如:  
* `libqlinuxfb.so` 用于 Frame Buffer
* `libqxcb.so` 用于 X11
* `libqwayland-generic.so` 用于 Wayland

构建 X11 插件需要依赖许多 xcb 的开发包，可以通过下面的命令安装:  

**Qt 5.15.2**:  
```bash
sudo apt install libfontconfig1-dev \
                 libfreetype6-dev \
                 libx11-dev \
                 libx11-xcb-dev \
                 libxext-dev \
                 libxfixes-dev \
                 libxi-dev \
                 libxrender-dev \
                 libxcb1-dev \
                 libxcb-glx0-dev \
                 libxcb-keysyms1-dev \
                 libxcb-image0-dev \
                 libxcb-shm0-dev \
                 libxcb-icccm4-dev \
                 libxcb-sync0-dev \
                 libxcb-xfixes0-dev \
                 libxcb-shape0-dev \
                 libxcb-randr0-dev \
                 libxcb-render-util0-dev \
                 libxcb-xinerama0-dev \
                 libxkbcommon-dev \
                 libxkbcommon-x11-dev
```

**Qt 6.5**:  
```
sudo apt install libfontconfig1-dev \
                 libfreetype6-dev \
                 libx11-dev \
                 libx11-xcb-dev \
                 libxext-dev \
                 libxfixes-dev \
                 libxi-dev \
                 libxrender-dev \
                 libxcb1-dev \
                 libxcb-cursor-dev \
                 libxcb-glx0-dev \
                 libxcb-keysyms1-dev \
                 libxcb-image0-dev \
                 libxcb-shm0-dev \
                 libxcb-icccm4-dev \
                 libxcb-sync-dev \
                 libxcb-xfixes0-dev \
                 libxcb-shape0-dev \
                 libxcb-randr0-dev \
                 libxcb-render-util0-dev \
                 libxcb-util-dev \
                 libxcb-xinerama0-dev \
                 libxcb-xkb-dev \
                 libxkbcommon-dev \
                 libxkbcommon-x11-dev
```

安装后重新构建即可:  

```bash
rm config.cache
./configure -nomake examples -prefix /opt/qt-6.5.2 -opensource -confirm-license -release -xcb
make
make install
```

单独编译某个模块的命令为:  

```bash
make module-qtbase                     # 单独编译 qtbase
make module-qtbase-install_subtargets  # 单独安装 qtbase
```

另外，如果需要 OpenGL 的话，可以安装以下包:  

```bash
sudo apt install libgl1-mesa-dev \
                 libglu1-mesa-dev \
                 libx11-dev
```

> 如果不需要 OpenGL 的话，在 configure 步骤添加  `-no-opengl` 选项即可。

如果需要使用 SSL 的话，可以安装以下包:

```bash
sudo apt install libssl-dev \
                 openssl
```
> 如果不需要 OpenGL 的话，在 configure 步骤添加  `-no-ssl` 选项即可。

**缓存问题**:  

执行过 configure 之后再安装依赖，再次执行 configure 仍会提示缺少依赖，可以删除 `config.cache` 来解决。 

**查找路径问题**:  

执行 configure 时可以使用 `-I` 和 `-L` 选项添加查找路径。

参考:  

* [Qt for X11 Requirements](https://doc.qt.io/qt-5/linux-requirements.html)