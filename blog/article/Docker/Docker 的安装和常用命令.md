# Docker 的安装和常用命令

## 安装 Docker

安装依赖
```bash
sudo apt install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
```

添加 docker 的 GPG key
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/docker.gpg
```

添加 docker 的 APT 源并更新
```bash
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
```

安装 docker
```bash
sudo apt install docker-ce docker-ce-cli containerd.io
```
* `ce` 表示社区版(Community Edition)
* `ee` 表示企业版(Enterprise Edition)

> 查看是否安装成功
> ```
> $ sudo docker version
> Client: Docker Engine - Community
>  Version:           20.10.23
>  API version:       1.41
>  Go version:        go1.18.10
>  Git commit:        7155243
>  Built:             Thu Jan 19 17:45:08 2023
>  OS/Arch:           linux/amd64
>  Context:           default
>  Experimental:      true
> 
> Server: Docker Engine - Community
>  Engine:
>   Version:          20.10.23
>   API version:      1.41 (minimum version 1.12)
>   Go version:       go1.18.10
>   Git commit:       6051f14
>   Built:            Thu Jan 19 17:42:57 2023
>   OS/Arch:          linux/amd64
>   Experimental:     false
>  containerd:
>   Version:          1.6.16
>   GitCommit:        31aa4358a36870b21a992d3ad2bef29e1d693bec
>  runc:
>   Version:          1.1.4
>   GitCommit:        v1.1.4-0-g5fd4c4d
>  docker-init:
>   Version:          0.19.0
>   GitCommit:        de40ad0
> ```

## 代理配置

创建或编辑 `/etc/systemd/system/docker.service.d/http-proxy.conf` 文件，写入以下内容:  

```conf
[Service]
Environment="ALL_PROXY=http://192.168.1.100:7890"
Environment="HTTP_PROXY=http://192.168.1.100:7890"
Environment="HTTPS_PROXY=http://192.168.1.100:7890"
```

然后重启:  

```
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## 常用命令

* 安装镜像: `image pull [OPTIONS] NAME[:TAG|@DIGEST]`   
* 删除镜像: `image rm [OPTIONS] IMAGE [IMAGE...]`  
* 运行容器: `container run [OPTIONS] IMAGE [COMMAND] [ARG...]`  
* 终止容器: `container stop [OPTIONS] CONTAINER [CONTAINER...]`

> 运行容器时通常使用前台和后台两种模式:  
> * 前台模式通常使用 `-it` 选项，其中:  
>   * `-i, --interactive` 表示保持 STDIN 打开， 
>   * `-t, --tty` 表示分配一个伪终端
> * 后台模式通常使用 `-d -p <host-port>:<container-port>` 选项，其中:  
>   * `-d, --detach` 表示后台运行
>   * `-p, --publish` 表示将容器端口公开到宿主机上

## 创建镜像

使用 `commit` 命令可以创建镜像，然后通过 `save` 命令可以将镜像保存到指定位置，通过 `load` 命令可以加载镜像文件。  
* 创建镜像: `container commit [OPTIONS] CONTAINER [REPOSITORY[:TAG]]`
* 保存镜像: `image save`，默认写到 stdout，可以通过 `-o` 指定文件
* 加载镜像: `image load`，默认读取 stdint，可以通过 `-i` 指定文件

## 自动补全的问题
> 使用 ubuntu 镜像时，会发现很多命令无法自动补全，需要安装 `bash-completion`
> ```
> apt install bash-completion
> source /etc/bash_completion
> ```

然后编辑 `/etc/bash.bashrc`  删除相关行的注释:  

```bash
# enable bash completion in interactive shells
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi
```