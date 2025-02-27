# Windows 程序添加图标


首先需要一个 `ico` 格式的图片，然后创建一个 `.rc` 的资源文件，内容如下：  

```
IDI_ICON1 ICON "icon.ico"
```

在 CMake 配置中将 `.rc` 资源文件添加到源码列表中:  

```cmake
add_executable(${PROJECT_NAME} ${SOURCE} icon.rc)
```

必须使用 `ico` 格式的图片，我写了一个转换工具： [萌萌工具箱 - 图片格式转换](https://hubenchang0515.github.io/moe-tools/#/image-format-convert)