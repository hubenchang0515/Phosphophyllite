# Python的异步IO

## 协程
Python 的异步 I/O 基于协程实现。使用`async`关键字来创建一个异步函数，对异步函数的调用不会执行该函数，而是生成一个协程对象。  
对每一个协程对象，都必须等待其结束(即使是没有启动的协程)，否则会产生一个`RuntimeWarning`。

示例 :  
```python
# 创建一个异步函数
async def say_hello():
    print("hello world")

# 创建协程
coro = say_hello()
print(coro)
```

运行结果 :  
```
<coroutine object say_hello at 0x109bf6170>
sys:1: RuntimeWarning: coroutine 'say_hello' was never awaited
```

要启动一个协程，有三种方式 :  
* 通过`asyncio.run`运行一个协程
* 使用`await`关键字，这种方法只能在另一个`async`函数中才能使用
* 通过`asyncio.create_task`

> `await`必须在`async`函数中才能使用，因此无法启动协程的顶层入口点，此时只能使用`asyncio.run`函数。
>
> `await`让出当前协程并运行目标协程，当前协程直到目标目标的状态变为`done`时才会恢复就绪。
> 如果`await`的目标不是一个协程(例如Task和Future)，让出当前协程后，事件循环(`EventLoop`)会从就绪队列中选择一个协程运行。
>
> `asyncio.create_task`让出当前协程并运行目标协程，当前协程不会等待而是加入就绪队列。  
> 只要目标协程让出，当前协程就有机会执行，从而将启动多个协程，实现并发执行。  
> 返回的`Task`对象也可以在适当的时候使用`await`等待其结束。

简化的协程状态 :  

![协程状态](https://user-images.githubusercontent.com/11847852/222871658-fdd0d4da-1c76-431c-b3d7-0aea36d75e93.png)

`await`的示例 :  
```python
import asyncio
import time

async def say_hello():
    print("hello", time.strftime('%X'))
    await asyncio.sleep(1)
    print("hello", time.strftime('%X'))

async def say_world():
    print("world", time.strftime('%X'))
    await asyncio.sleep(1)
    print("world", time.strftime('%X'))

# 顶层入口点
async def main():
    await say_hello() # 启动say_hello()返回的协程，并等待其结束
    await say_world() # 要等到前一个await结束后，才会启动

# 启动顶层入口点
asyncio.run(main())
```

运行结果 :  
```
hello 15:27:26
hello 15:27:27
world 15:27:27
world 15:27:28
```

`asyncio.create_task`的示例 :  
```python
import asyncio
import time

async def say_hello():
    print("hello", time.strftime('%X'))
    await asyncio.sleep(1)
    print("hello", time.strftime('%X'))

async def say_world():
    print("world", time.strftime('%X'))
    await asyncio.sleep(1)
    print("world", time.strftime('%X'))

# 顶层入口点
async def main():
    task_say_hello = asyncio.create_task(say_hello()) # 启动协程不等待
    task_say_world = asyncio.create_task(say_world()) 

    await task_say_hello
    await task_say_world

# 启动顶层入口点
asyncio.run(main())
```

运行结果 :  
```
hello 15:29:41
world 15:29:41
hello 15:29:42
world 15:29:42
```

通过上面两个示例打印的顺序和时间可以看出`await`和`asyncio.create_task`的区别

本来准备介绍一下`asyncio`中的TCP和UDP接口，但是抄袭官方文档没有意义，而且我懒得写了，下面是一个TCP server的示例，旨在演示如何使用协程并发处理客户请求。

在`/block`的请求处理函数中有一个延时10秒的操作(`await asyncio.sleep(delay)`)，但是因为使用异步操作进行，所有不需要等待它结束就能相应其它请求。
* `await asyncio.sleep(delay)`将当前协程让出，运行`asyncio.sleep(delay)`返回的协程。
* `asyncio.sleep(delay)`返回的协程里，会创建一个`Future`对象，并在`EventLoop`中注册(`EventLoop`将在`delay`秒后将`Future`对象的状态设为`done`
)，之后`await future`让出，等待`future`的状态变为`done`。
* 由于目标不是协程，`EventLoop`会从就绪队列中选取一个协程来运行，因此可以对新的请求做出相应。

```python
import asyncio
import re

class DemoProtocol(asyncio.Protocol):
    # 获取url的正则
    url_re = re.compile(b'GET (.*) HTTP/1.1')

    # 连接创建时的回调函数
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    # 收到数据时的回调函数
    def data_received(self, data):
        # 获取url
        url = DemoProtocol.url_re.match(data).group(1)
        print("GET", url)
        # 根据url做不同的处理
        if url == b"/block" :
            # 10s后响应
            asyncio.create_task(self.response_after(b'<h1>Are you block?</h1>', 10))
        else:
            asyncio.create_task(self.response(b'<h1>hello world</h1>'))

    # 立刻返回响应
    async def response(self, content):
        self.transport.write(b"HTTP/1.1 200 OK\r\n")
        self.transport.write(b"Content-Type: text/html\r\n")
        self.transport.write(b"\r\n")
        self.transport.write(content)
        self.transport.write(b"\r\n")
        self.transport.close()

    # 延迟返回响应
    async def response_after(self, content, delay):
        await asyncio.sleep(delay)
        await self.response(content)


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(lambda: DemoProtocol(), '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()

asyncio.run(main())
```