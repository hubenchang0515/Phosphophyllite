# 部署 GitLab 和持续集成环境

参考: https://about.gitlab.com/install/

## 部署 Gitlab

安装依赖:  

```bash
sudo apt update
sudo apt install -y curl openssh-server ca-certificates tzdata perl postfix
```

添加 Gitlab 的仓库（以debian为例）:  

```bash
curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | sudo bash
```

安装 Gitlab 的包:  

```bash
sudo EXTERNAL_URL="https://gitlab.example.com" apt install gitlab-ce
```

> 把 `gitlab.example.com` 替换成你将要使用的域名，如果你没有域名可以配置为 HOSTNAME，例如 `raspberrypi.local`
>
> 如果域名发生了改变，在 `/etc/gitlab/gitlab.rb` 文件中进行修改

访问 Gitlab 页面:  

安装完成后即可从浏览器访问，管理员账户的用户名为 `root`，初始密码保存在 `/etc/gitlab/initial_root_password` 文件中。

登录后应当立即修改密码。

![gitlab-password](https://raw.githubusercontent.com/hubenchang0515/resource/master/gitlab/gitlab-password.png)

## 持续集成（CI）

### 部署 Gitlib CI 运行环境

安装 `gitlab-runner` :  

```bash
sudo curl -L --output /usr/local/bin/gitlab-runner https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-arm64

sudo chmod +x /usr/local/bin/gitlab-runner

sudo useradd --comment 'GitLab Runner' --create-home gitlab-runner --shell /bin/bash

sudo gitlab-runner install --user=gitlab-runner --working-directory=/home/gitlab-runner

sudo gitlab-runner start
```

在 `Admin Area -> CI/CD ->  Runners` 页面，点击 `New instance runner` 按钮创建 Runner

然后根据页面提示执行命令配置 TOKEN:  

```bash
sudo gitlab-runner register --url http://raspberrypi.local --token glrt-n3W91JCVxCNRs6qJzVfM
```

### 为项目配置 CI 工作流

在项目的根目录中创建 `.gitlab-ci.yml` 文件，例如:  

```yml
# 作业的名字是 default
default:

    # 执行 echo hello world
    script: echo hello world
```

每次项目推送到 Gitlab 服务器上或者发起 pull-request 时，都会执行根据该配置执行步骤。

![gitlab-pipeline](https://raw.githubusercontent.com/hubenchang0515/resource/master/gitlab/gitlab-pipeline.png)

![gitlab-job](https://raw.githubusercontent.com/hubenchang0515/resource/master/gitlab/gitlab-ci-helloworld.png)

一个简单的 CMake 项目 CI 配置示例:

```yml
# 作业1:构建
Build:
  script:
    - mkdir build
    - cd build
    - cmake ..
    - make

# 作业2:构建单元测试并生成覆盖率报告
Coverage:
  script:
  - mkdir build
  - cd build
  - cmake .. -DUNIT_TEST=ON           # 具体根据 CMakeLists.txt 内容进行配置
  - make
  - ./test/silk_unit_test
  - lcov -c -d . -o coverage.info --rc lcov_branch_coverage=1   # 具体根据单元测试工具进行配置
  - genhtml --branch-coverage -o ./coverage coverage.info
```

这个示例创建了两个 CI Jobs，分别名为 Build 和 Coverage:  

* Build - 进行构建
* Coverage - 构建单元测试并运行，然后生成覆盖率报告

![gitlab-ci-jobs](https://raw.githubusercontent.com/hubenchang0515/resource/master/gitlab/gitlab-ci-jobs.png)

![gitlab-ci-coverage](https://raw.githubusercontent.com/hubenchang0515/resource/master/gitlab/gitlab-ci-coverage.png)

