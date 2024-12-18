# 制作deb包

安装工具

```bash
sudo apt-get install build-essential
sudo apt-get install debmake
```

配置作者的邮箱和名字

```bash
export DEBEMAIL="hubenchang0515@outlook.com"
export DEBFULLNAME="PlanC"
```

生成 `debian` 目录

```bash
debmake -n
```