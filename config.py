from typing import Set, Dict

# web服务的IP端口
host:str = "0.0.0.0"
port:int = 5000

# 调试模式
debug:bool = False

# 数据库配置
sql_url:str = "postgresql://pi:123456@localhost/phosphophyllite"

# 浏览器身份
user_agent:str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36" 

# 从这些链接开始爬
entry_urls:Set[str] = {
    "https://zh.wikipedia.org/",
    "https://www.qq.com/",
    "http://www.163.com/",
    "https://www.zhihu.com/explore",
    "https://www.sina.com.cn/",
    "https://www.sohu.com/",

}

# 代理
proxy:Dict[str, str] = {
    "http": None,
    "https": None
}

# 待爬url队列最大长度
spider_queue_max_size:int = 99999

# 爬取页面的最大字节数
web_page_max_size:int = 100 * 1024 * 1024

# 爬取同一个网站的冷却时间，秒
cd:int = 24 * 60 * 60

# 请求的超时时间，秒
timeout:int = 5