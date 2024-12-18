# OpenGL 选择使用独立显卡

OpenGL 没有手动选择显卡的 API，在同时具备核心显卡和独立显卡的设备上常常会在核显上运行。

Windows 上可以添加如下代码选择使用独显:  

```cpp
#ifdef __cplusplus
extern "C" {
#endif

#ifdef _MSC_VER
    __declspec(dllexport) uint32_t NvOptimusEnablement = 1;
    __declspec(dllexport) int AmdPowerXpressRequestHighPerformance = 1;
#else 
    uint32_t NvOptimusEnablement = 1;
    int AmdPowerXpressRequestHighPerformance = 1;
#endif

#ifdef __cplusplus
}
#endif
```

Linux 上可以配置如下环境变量选择使用 NVIDIA 的独显:  

```
export __NV_PRIME_RENDER_OFFLOAD=1 
export __GLX_VENDOR_LIBRARY_NAME=nvidia
```

NVIDIA 和 AMD 显卡的驱动会分别检查程序中这两个全局变量的值来决定是否使用

> NVIDIA 显卡可以在 `NVIDIA 控制面板 -> 管理 3D 设置 -> 首选图形处理器` 中选择使用核显、独显、自动。  

## 扩展接口

* [WGL_NV_gpu_affinity](https://registry.khronos.org/OpenGL/extensions/NV/WGL_NV_gpu_affinity.txt)
* [WGL_AMD_gpu_association](https://registry.khronos.org/OpenGL/extensions/AMD/WGL_AMD_gpu_association.txt)