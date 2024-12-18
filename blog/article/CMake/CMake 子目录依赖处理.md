# CMake 子目录依赖处理

最近开发的一个项目依赖 `libgeotiff`，同时 `libgeotiff` 又依赖 `libtiff`，我将他们都加入 thirdparty 中，通过 `add_subdirectory` 添加进项目中。

* thirdparty
  * CMakeLists.txt
  * libgeotiff
  * libtiff

```cmake
add_subdirectory(libtiff)
add_subdirectory(libgeotiff/libgeotiff)
```

这样 CMake 仍会报错:  

```
CMake Error at /usr/local/lib/python3.10/dist-packages/cmake/data/share/cmake-3.25/Modules/FindPackageHandleStandardArgs.cmake:230 (message):
  Could NOT find TIFF (missing: TIFF_LIBRARY TIFF_INCLUDE_DIR)
```

因为 `find_package` 无法查找项目内的目标。

可以通过 `FetchContent` 来解决这个问题:  

```cmake
include(FetchContent)
FetchContent_Declare(
    TIFF
    SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/libtiff"
    OVERRIDE_FIND_PACKAGE
)
add_subdirectory(libgeotiff)
```