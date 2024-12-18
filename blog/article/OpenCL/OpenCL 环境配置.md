# OpenCL 环境配置

## Intel

安装 [Intel-OpenCL-SDK](https://software.intel.com/content/www/us/en/develop/tools/opencl-sdk/choose-download.html)

## AMD

安装 [AMD-APP-SDK](https://stackoverflow.com/questions/53070673/download-opencl-amd-app-sdk-3-0-for-windows-and-linux) 或 [ROCm](https://www.amd.com/zh-hans/graphics/servers-solutions-rocm) 

* AMD-APP-SDK 的下载链接已经被AMD删除,需要从其它地方下载
* ROCm 暂不支持Windows,并且不支持核显

## NVIDIA

安装[显卡驱动](https://www.nvidia.com/download/index.aspx?lang=en-us) 和 [CUDA开发包](https://developer.nvidia.com/cuda-downloads)

## 遇到的一些问题

> Q: fatal error: `CL/cl2.hpp`: no such file or directory  
> A: sudo apt install opencl-headers  

> Q: /usr/bin/ld: cannot find `-lOpenCL`  
> A: sudo apt install ocl-icd-*

> Q: failed to create context  
> A: sudo apt reinstall beignet