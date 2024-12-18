# Windows 上 CMake 找不到 CUDA 工具集的问题

## 问题1  
```
CMake Error at C:/Program Files/CMake/share/cmake-3.22/Modules/CMakeDetermineCompilerId.cmake:470 (message):
  No CUDA toolset found.
```

需要将 CUDA 目录里的 MSBuildExtensions 赋值 Visual Studio 的目录中:  

```
cp "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.5\extras\visual_studio_integration\MSBuildExtensions\*" "C:\Program Files\Microsoft Visual Studio\2022\Community\Msbuild\Microsoft\VC\v170\BuildCustomizations"
```

## 问题2

```
The CUDA compiler identification is unknown
CMake Error at src/matrix/cuda/CMakeLists.txt:2 (project):
  No CMAKE_CUDA_COMPILER could be found.
```

这是因为 CUDA 不支持 32 位，需要添加 `-A x64` 指定构建 64 位目标。

> 另外 CUDA 11.5 只支持 VS2017 - VS2019，因此使用 VS2022 也会报这个错误，需要升级 CUDA 版本。