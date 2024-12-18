# Jetson Nano 系统安装配置

1. 从 [Jetson Download Center](https://developer.nvidia.com/embedded/downloads) 下载 [系统镜像](https://developer.nvidia.com/embedded/l4t/r32_release_v7.1/jp_4.6.1_b110_sd_card/jeston_nano/jetson-nano-jp461-sd-card-image.zip)
2. 使用镜像烧录软件（如 [Rufus](https://rufus.ie/) 等）将镜像烧录到内存卡上。
3. 将内存卡插到 Jetson 上，插电自动开机，配置都使用默认值即可。
4. Jetson 的镜像预装了 CUDA，但是运行 `nvcc` 会提示找不到，将 `/usr/local/cuda/bin/` 加入 PATH 环境变量即可。