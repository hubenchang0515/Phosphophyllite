# 找不到 config.guess 和 config.sub 文件

现象:  

```
configure: error: cannot find required auxiliary files: config.guess config.sub
```

解决办法:  

```
automake --add-missing
```