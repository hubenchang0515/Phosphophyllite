# NPM 镜像源配置

```bash
# 当前用户
npm config set registry https://registry.npmmirror.com

# ROOT
sudo npm config set registry https://registry.npmmirror.com
```


## 发生的问题

**错误消息**

```
npm ERR! Cannot read property 'insert' of undefined
```

这是因为配置了错误的地址，下载失败导致的。

**解决办法**

```bash
# 当前用户
npm cache clear --force
npm config set registry https://registry.npmmirror.com

# ROOT
sudo npm cache clear --force
sudo npm config set registry https://registry.npmmirror.com
```