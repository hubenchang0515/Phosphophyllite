# 制作 deb 包

参考 [QtTheme](https://github.com/hubenchang0515/QtTheme/)

## 准备工作

安装工具：

```bash
sudo apt-get install build-essential
sudo apt-get install debmake
```

配置作者的邮箱和名字：

```bash
export DEBEMAIL="hubenchang0515@outlook.com"
export DEBFULLNAME="planc"
```

## 初始化项目

通过 `debmake` 生成 `debian` 目录：  

```bash
debmake -e hubenchang0515@outlook.com -p qttheme -u 1.0.0 -n
```

## 打包


执行 `debuild` 命令进行打包：  

```
debuild
```

## 更新版本

在 `debian/changelog` 最上方添加一条空的 `changelog` ：  

```
qttheme (1.0.1) UNRELEASED; urgency=low

 -- planc <hubenchang0515@outlook.com>
```

执行 `dch -v 1.0.1` 命令，编辑 `changelog` 的内容，最后保存，会自动生成时间。