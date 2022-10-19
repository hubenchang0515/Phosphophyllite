# Phosphophyllite
lightweight search engine backend - 轻量级搜索引擎后端

结构:  

![phos-struct](./doc/image/phos-struct.png)

运行 `python3 main.py` 即可启动:  

![phos](./doc/image/phos.png)

## API

URL Path: `/api/search`

参数:  

| query        | page   | page_size             |
| :-:          | :-:    | :-:                   |
| 搜索的内容   | 第几页 | 每页显示多少条搜索结果 |

返回值:  
```json
{
    "query": "query",       // 搜素的内容
    "page": 0,              // 第几页
    "page_size": 20,        // 每页显示多少条搜索结果
    "page_count": 1,        // 总共有多少页

    // 搜索结果列表
    "web_page_list": [
        {
            "url": "...",           // 网页的URL
            "title": "",            // 网页的标题
            "update_time": "...",   // 网页被爬取的时间
            "content": "...",       // 网页的内容
            "matched_keywords": []  // 网页匹配到的关键词
        }
    ]
}
```

示例:  

![phos-api](./doc/image/phos-api.png)  

## 预览

此项目附带一个简单的预览界面，访问 `/preview/search` 即可查看:  

![phos-preview](./doc/image/phos-preview.png)  



## 数据库

> 这个项目不能使用 SQLite，因为它不能并行访问。而搜索引擎需要在不断爬取网络上页面的同时提供搜索服务。

以 PostgreSQL 为例，安装并配置数据库
```
pi@raspberrypi:~ $ sudo apt install postgresql                      # 安装 postgresql
pi@raspberrypi:~ $ sudo su postgres                                 # 切换到 postgres
postgres@raspberrypi:~$ psql                                        # 进入 postgresql 命令行
postgres=# CREATE USER pi WITH PASSWORD '123456';                   # 创建用户并设置密码
postgres=# CREATE DATABASE phosphophyllite OWNER pi;                # 创建数据库
postgres=# GRANT ALL ON DATABASE phosphophyllite TO pi;             # 将该数据库的所有权限授予用户
postgres=# \q                                                       # 退出 postgresql 命令行
```

编辑配置文件
```python
sql_url = "postgresql://pi:123456@localhost/phosphophyllite"
```

