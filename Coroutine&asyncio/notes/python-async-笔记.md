---
title: python async 笔记
date: 2023-05-21 19:11:13
tags: Python
---

## 1. 协程

协程（Coroutine）不是操作系统提供的，是人为创造的。是一种用户态内的上下文切换技术，通过一个线程实现代码块相互切换执行。

<!--more-->

实现协程的方法：

* yield关键字
* asyncio装饰器
* async，await 关键字【推荐】

### 1.1 asyncio

在python3.4及以后的版本。

```python
import asyncio


@asyncio.coroutine
def func1():
    print(1)
    yield from asyncio.sleep(2)  # 遇到IO操作耗时，自动切换到tasks中的其他任务
    print(2)


@asyncio.coroutine
def func2():
    print(3)
    yield from asyncio.sleep(2)  # 遇到IO操作耗时，自动切换到tasks中的其他任务
    print(4)


tasks = [
    asyncio.ensure_future(func1()),
    asyncio.ensure_future(func2())
]

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

```

### 1.2 async & await关键字

在python3.5及以后的版本。

```python
import asyncio


async def func1():
    print(1)
    await asyncio.sleep(2)  # 遇到IO操作耗时，自动切换到tasks中的其他任务
    print(2)


async def func2():
    print(3)
    await asyncio.sleep(2)  # 遇到IO操作耗时，自动切换到tasks中的其他任务
    print(4)


tasks = [
    asyncio.ensure_future(func1()),
    asyncio.ensure_future(func2())
]

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
```

## 2. 协程意义

在一个线程中如果遇到IO等待时间，线程不会等待，会利用空闲的时间去做其他操作。

如：下载图片（网络IO）

* 普通方式

  ```python
  import requests
  
  
  def download_pic(url: str):
      response = requests.get(url)
      file_name = url.rsplit("_")[-1]
      with open(file_name, 'wb') as file_obj:
          file_obj.write(response.content)
  
  
  if __name__ == '__main__':
      url_list = []
      for url in url_list:
          download_pic(url)
  ```

* 异步方式

  ```python
  import requests
  import aiohttp
  import asyncio
  
  
  async def fetch(session, url):
      async with session.get(url) as response:
          content = await response.content.read()
          file_name = url.rsplit("_")[-1]
          with open(file_name, 'wb') as file_obj:
              file_obj.write(content)
  
  
  async def main():
      async with aiohttp.ClientSession() as session:
          url_list = []
          tasks = [asyncio.create_task(fetch(session, url)) for url in url_list]
          await asyncio.wait(tasks)
  
  
  if __name__ == '__main__':
      asyncio.run(main())
  ```

## 3. 异步编程

### 3.1 事件循环

一个死循环，检测并执行某些代码。

```
# pseudo code

task_list = [task1, task2, task3...]

while True:
	Executable list, finished list = Check all tasks in the list
	
	for executable task:
		execute task
	
	for finished task:
		remove task from task list
	
	if all tasks are finished:
		break
```

```python
if __name__ == '__main__':
    # 生成事件循环
    loop = asyncio.get_event_loop()
    # 将任务放到任务列表中
    loop.run_until_complete(asyncio.wait(tasks))
```

### 3.2 基本概念

协程函数：在函数前加上`async`。

协程对象：执行协程函数得到的对象

```python
async def func():
    pass

res = func()
```

创建协程对象后，函数内部代码不会执行。

```python
async def func():
    pass

res = func()

# loop = asyncio.get_event_loop()
# loop.run_until_complete( res )
asyncio.run(res) # python3.7之后出现
```

### 3.3 await

await + 可等待的对象（协程对象，Future, Task对象）

示例1:

```python
import asyncio


async def func():
    print(1)
    response = await asyncio.sleep(2)
    print("2", response)


if __name__ == '__main__':
    asyncio.run(func())
```

示例2：

```python
import asyncio

async def others():
    print("start")
    await asyncio.sleep(2)
    print("end")
    return 1


async def func():
    print("start func")
    response1 = await others()
    print("end func, response1 = ", response1)
    response2 = await others()
    print("end func, response2 = ", response2)


if __name__ == '__main__':
    asyncio.run(func())
```

await会等待对象得到返回值后再继续执行

### 3.4 Task对象

Task对象用来并发地调度协程，当一个协程被包装到了一个Task中后，这个协程会自动加入事件循环并等待执行，一般用`asyncio.create_task(协程对象)`创建Task。

```python
import asyncio


async def func():
    print(1)
    await asyncio.sleep(2)
    print(2)
    return 3


async def main():
    print("start main")
    task_list = [
        asyncio.create_task(func()),
        asyncio.create_task(func())
    ]
    print("end main")
    done, pending = await asyncio.wait(task_list)
    print(done)


if __name__ == '__main__':
    asyncio.run(main())
```

### 3.5 Future对象

Future对象代表了异步操作的最终结果，Task继承Future，Task对象内部await结果的处理基于Future对象。

```python
import asyncio


async def set_after(fut):
    await asyncio.sleep(2)
    fut.set_result("2")


async def main():
    # 获取当前事件循环
    loop = asyncio.get_running_loop()
    # 创建一个Future对象
    fut = loop.create_future()
    # 创建一个任务对象，其中的函数会给Future赋值并返回，这样Future就会结束了
    await loop.create_task(set_after(fut))
    # 等待Future对象最终结果
    data = await fut
    print(data)


if __name__ == '__main__':
    asyncio.run(main())
```

### 3.6 concurrent中的Future对象

使用线程池、进程池实现异步操作的时候会用到的对象。

```python
import time
from concurrent.futures.thread import ThreadPoolExecutor


def func(value):
    time.sleep(1)
    print(value)


# 创建线程池
pool = ThreadPoolExecutor(max_workers=1)

if __name__ == '__main__':
    for i in range(10):
        fut = pool.submit(func, i)
        print(fut)
```

在开发过程中可能会存在同时用到协程和线程池的情况。一般我们使用协程，但有些模块不支持协程，如一些和数据库交互的模块，就需要使用线程和进程进行异步操作。

```python
import asyncio
import time


def func():
    time.sleep(1)
    return "result"


async def main():
    loop = asyncio.get_running_loop()
    # 把func包装到Future中，放到线程池中
    fut = loop.run_in_executor(None, func)
    res = await fut
    print("default thread pool", res)


if __name__ == '__main__':
    asyncio.run(main())
```

### 3.7 上下文管理器

对象通过定义`__aenter__`和`__aexit__`方法来控制上下文。

```python
import asyncio


class ContextManager:
    def __init__(self):
        self.conn = None

    async def func(self):
        # 异步操作数据库
        return 1

    async def __aenter__(self):
        # 异步连接数据库
        self.conn = await asyncio.sleep(1)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # 异步关闭连接
        await asyncio.sleep(1)


async def main():
    async with ContextManager() as f:
        res = await f.func()
        print(res)


if __name__ == '__main__':
    asyncio.run(main())
```

## 4. 案例

### 4.1 异步操作redis

在用Python操作redis时，连接、操作、断开都可以用异步编程。

```python
import aioredis
import asyncio


async def func(address, pwd):
    print("start process")

    redis = await aioredis.create_redis(address, pwd)

    await redis.set('car', 1)

    redis.close()

    await redis.wait_closed()

    print("end")
```

### 4.2 异步MySQL

```python
import aiomysql
import asyncio


async def func():
    conn = await aiomysql.connect()

    cur = await conn.cursor()

    await cur.execute("")

    res = await cur.fetchall()

    await cur.close()
    conn.close()
    return res
```

## 5. 总结

异步的意义：通过一个线程利用其IO等待时间去做其他事情。
