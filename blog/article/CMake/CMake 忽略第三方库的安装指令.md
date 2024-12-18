# CMake 忽略第三方库的安装指令

通过 CMake 在项目中包含第三方库的源码时，如果直接包含，install 的时候会同时安装第三方库。如果不想安装第三方库，可以添加 `EXCLUDE_FROM_ALL`

```CMake
add_subdirectory(${目录} EXCLUDE_FROM_ALL)
```