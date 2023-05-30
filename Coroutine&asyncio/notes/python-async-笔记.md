---
title: python async 笔记
date: 2023-05-21 19:11:13
tags: Python
---

Asyncio让我们可以通过协程进行异步编程。

协程（Coroutine）不是操作系统提供的，是人为创造的。是一种用户态内的上下文切换技术，通过一个线程实现代码块相互切换执行。

<!--more-->

# 什么是异步编程

异步编程是指非阻塞的编程。‘

### 异步任务

异步意味着函数被请求了，但是不立即执行，而是之后被执行，我们可以之后检查异步任务的状态和结果。这个函数会在某个时刻在底层进行，程序可以进行别的任务。

### 异步编程

异步编程指的是执行异步任务和调用异步方法，主要用于非阻塞IO。IO操作会在系统级别进行，调用者不用等待IO操作结束就可以返回，可以在之后查看异步任务的状态和结果

### python中的异步编程

我们可以有多种方法来实现异步编程，通过`Asyncio`，线程池来实现。

# 什么是Asyncio

实现协程的方法：

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

# 什么时候使用Asyncio

### 使用Asyncio的原因

总的来说，使用Asyncio有以下三个原因。

#### 1. 为了使用协程

如果我们希望通过协程来实现并发，和线程、进程并发类似。

线程并发主要用于阻塞IO。

进程并发主要用于不需要彼此交互的CPU-bound任务，比如计算任务

协程通常适用于非阻塞IO，不过也可以支持阻塞IO和CPU-bound任务（不推荐），任何通过线程和进程开发的程序都可以用协程来改写。

线程和进程通过操作系统来选择哪个线程/进程应该运行，操作系统会在不同线程/进程之间进行切换。被称为抢占式多任务处理。

协程则被称为合作式多任务处理，可以被暂停和恢复，我们可以设计协程什么时候以及以什么方式暂停，这相对于线程和进程，给了我们更多控制的空间。同时，协程比线程需要更少的资源，相较于线程，我们可以有更多的协程同时运行，可扩展性更强。

#### 2. 为了异步编程

Asyncio可以以异步的形式来进行阻塞IO和CPU-bound任务。

#### 3. 为了非异步IO

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

### 什么情况不适合Asyncio

首先，在我们不需要异步编程的时候，比如我们在面向过程编程，或者当前程序不需要大量的IO操作，是不需要使用Asyncio的。同时，Asyncio不适合CPU密集型任务。

并且，一个线程中同时只有一个协程可以运行，几乎所有的协程写的代码都可以用线程来实现，在某些情况下，线程会比协程效率更高，并且更加容易理解。

# Python中的协程

协程可以认为是一个生成的子线程，协程可以被执行、暂停和恢复，多个协程可以被同时创建和运行，我们可以控制这些协程什么时候暂停和恢复，这被称为合作式多任务处理。

### 协程和线程的区别

一个线程可以包括多个线程。

协程比线程更加轻量级。协程通过方法定义，协程是一个操作系统创建并管理的对象。

协程需要更少的内存，所以通常比线程更加快的创建并执行。

# 协程的定义、创建和运行

### 定义协程

可以通过`async def`表达式来定义协程。

```python
async def func():
    pass
```

### 创建协程

协程定义之后，可以创建一个协程对象，如

```python
async def func():
    pass

res = func()
```

创建协程并不会执行协程。

### 运行协程

协程被定义和创建之后，需要在事件循环中运行。事件循环可以用来执行协程任务，管理不同协程之间的多任务处理。一个常用的开始事件循环的方法是`asyncio.run()`方法。这个方法接收协程并返回协程的返回值。

```python
import asyncio
# define a coroutine
async def custom_coro():
    # await another coroutine
    await asyncio.sleep(1)
 
# main coroutine
async def main():
    # execute my custom coroutine
    await custom_coro()
 
# start the coroutine program
asyncio.run(main())
```

# 事件循环



实现协程的方法：

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

### 

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
