# Python 虚拟环境与依赖导出

因为不同的项目之间可能存在依赖冲突，因此需要使用虚拟环境，避免在全局环境上安装依赖。

## Python 依赖导出

通过 `pipreqs` 可以将当前项目依赖的所有包导出到 `requirements.txt` 中：

```
$ pipreqs . --encoding=utf8 --force 
```

> 注意，如果在当前路径下配置了虚拟环境，pipreqs 会读取寻环境的目录产生多余的依赖，需要添加 `--ignore .venv` 参数来消除影响  
> 可以使用 `--proxy http://localhost:7890` 来配置代理

然后通过该文件即可一键安装所有依赖

```
$ pip install -r requirements.txt
```

## virtualenv

1. 安装
```
pip install virtualenv
```

2. 创建
```
virtualenv [虚拟环境名称] 
```

3. 激活
```
cd [虚拟环境目录]
source ./bin/activate
```


4. 退出
```
deactivate
```
## pipenv

1. 安装
```
pip install pipenv
```

2. 创建
```
pipenv install
```
> 在项目目录里执行，如果没有 `pipfile`，则会创建；如果有则会安装记录在当中的依赖

3. 安装依赖包
```
pipenv install [包名]
```
> 在项目目录里执行，安装依赖的同时记录到 `pipfile` 中去，如果文件不存在则自动创建

4. 激活
```
pipenv shell
```

---
> 另外还有 `virtualenvwrapper`、`conda` 可以管理虚拟环境，此处暂不列出。