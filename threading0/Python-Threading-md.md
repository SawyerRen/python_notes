---
title: Python Threading.md
date: 2023-05-28 11:27:25
tags: Python
---

Python `Threading` 模块可以创建线程并管理线程的执行，本文包括线程如何运行，怎么在多线程编程中使用线程，线程同步，常见问题和最佳实践。

<!--more-->

# Python线程

### 什么是线程？

线程是程序运行的一个单位，每个程序都至少有一个线程在执行进程的内容。当我们运行一个Python程序，我们会在Python编译器中开始一个实例，并且在Main线程中运行代码。Main线程是Python的默认线程。

我们可以让程序并发的运行，这样我们需要创建并运行新的线程。一个Python线程是操作系统提供的线程的代表，当我们创建一个线程，Python会创建一个操作系统级别的线程并且运行代码。这表明Python线程是真实的线程，而不是模拟出的软件线程。

即使这些线程并行的运行，线程中的代码可能会并行的运行，也可能不会，这取决于底层的硬件是否支持并行运行，Python编译器是否支持并行。也就是说，代码会并发(**Concurrent**)运行，但不一定并行(**Parallel**)。

### 线程与进程

进程是一个计算机程序。一个进程是一个Python编译器的实例，正在执行Python指令。

一个线程存在于进程中，是一个进程执行代码的单位。

### 线程的Life-Cycle

Python中的线程由Thread类代表。一个线程开始后，Python编译器会和操作系统交互并创建一个线程实例。

每个线程的Life-Cycle都是相同的，一个Python线程可以分为3个步骤：一个新线程，一个正在运行的线程，和一个已经终止的线程。当一个线程正在运行时，可能会被阻塞(blocked)，等待其他线程或者外部资源。

1. New Thread.
2. Running Thread.
   1. Blocked Thread (optional).
3. Terminated Thread.

![Thread-Life-Cycle](https://superfastpython.com/wp-content/uploads/2022/03/Thread-Life-Cycle.png)

# 在线程中运行函数

### 怎么在线程中运行函数？

步骤：

1. 创建一个` threading.Thread`对象
2. 在`target`参数中确定运行的函数
3. 运行`start()`方法

运行的函数的参数可以通过`args`参数来传入。

`start()`方法会立刻返回，操作系统会安排一个线程来执行target方法。我们无法控制哪一个CPU core来执行这个程序，也不能控制这个方法什么时候执行。

### 在线程中执行函数的例子

首先我们定义一个执行的函数。

```python
# a custom function that blocks for a moment
import time


def task():
    # block for a moment
    time.sleep(1)
    # display a message
    print('This is from another thread')
```

接下来，我们创建一个Thread对象，并且将这个函数传入到`target`中，然后我们可以运行这个线程，系统会创建一个线程来执行这个函数。我们可以通过`join()`方法来等待这个线程的执行（在这个例子中，我们实际上不需要join方法，因为Main线程会自动等待所有线程完成再结束）。

```python
from time import sleep
from threading import Thread


# a custom function that blocks for a moment
def task():
    # block for a moment
    sleep(1)
    # display a message
    print('This is from another thread')


if __name__ == '__main__':
    # create a thread
    thread = Thread(target=task)
    # run the thread
    thread.start()
    # wait for the thread to finish
    print('Waiting for the thread...')
    thread.join()
```

注意，`start()`方法不会直接运行`task()`，而是会让操作系统安排尽早地执行`task()`函数。Main线程会打印信息，并且等待其他线程执行结束。

```
Waiting for the thread...
This is from another thread
```

### 在线程中执行带参数的函数的例子

我们把`task()`函数修改，可以传入两个参数

```python
# a custom function that blocks for a moment
def task(sleep_time, message):
    # block for a moment
    sleep(sleep_time)
    # display a message
    print(message)
```

我们将这两个参数通过`args`传入`Thread`类的构造方法。

```python
from time import sleep
from threading import Thread
 
# a custom function that blocks for a moment
def task(sleep_time, message):
    # block for a moment
    sleep(sleep_time)
    # display a message
    print(message)
 
# create a thread
thread = Thread(target=task, args=(1.5, 'New message from another thread'))
# run the thread
thread.start()
# wait for the thread to finish
print('Waiting for the thread...')
thread.join()
```

# Thread对象的属性

### Thread.name

每个线程都有一个名字，如果不特意指定，线程的名字自动被命名为`Thread-%d`，%d是进程中的线程计数，比如，`Thread-1`是创建的第一个线程。

```python
from threading import Thread
# create the thread
thread = Thread()
# report the thread name
print(thread.name)
```

返回

```
Thread-1
```

我们可以传入`name`参数来指定线程名字

```python
thread = Thread(name='MyThread')
```

### Thread.daemon

一个线程可能是一个服务线程，一个线程默认不是服务线程。一个Python程序只有在所有的非服务线程都结束了之后结束。而服务线程会在底层运行，不需要在Python程序结束之前结束。

```python
from threading import Thread
# create the thread
thread = Thread()
# report the daemon attribute
print(thread.daemon)
```

返回False因为线程默认是非服务线程。

```
False
```

我们可以传入`daemon`参数来指定是否是服务线程

```python
# create a daemon thread
thread = Thread(daemon=True)
```

### Thread.ident

每个线程都有一个id，会在线程开始后被赋给这个线程。

```python
from threading import Thread
# create the thread
thread = Thread()
# report the thread identifier
print(thread.ident)
# start the thread
thread.start()
# report the thread identifier
print(thread.ident)
```

只有在线程`start()`之后，才会生成一个id。

```
None
123145502363648
```

### Thread.native_id

每个线程都有一个操作系统的唯一id。

```python
from threading import Thread
# create the thread
thread = Thread()
# report the native thread identifier
print(thread.native_id)
# start the thread
thread.start()
# report the native thread identifier
print(thread.native_id)
```

和`ident`属性一样，只有在线程`start()`之后，才会生成一个id。

```
None
3061545
```

### Thread.is_alive

用来表示一个线程是否还在运行，即`start()`之后到`run()`方法结束之前。

```python
from time import sleep
from threading import Thread
# create the thread
thread = Thread(target=lambda:sleep(1))
# report the thread is alive
print(thread.is_alive())
# start the thread
thread.start()
# report the thread is alive
print(thread.is_alive())
# wait for the thread to finish
thread.join()
# report the thread is alive
print(thread.is_alive())
```

在`start()`之前，和`join()`之后，都返回False

```
False
True
False
```

# Main线程

每个python进程都有一个默认的线程：main 线程。在main线程退出的时候，python进程也就结束了。我们在main线程中可以通过`threading.current_thread()`来获得main线程，或者用`threading.main_thread()`方法在任何线程中获得main线程。

```python
from threading import current_thread
# get the main thread
thread = current_thread()
# report properties for the main thread
print(f'name={thread.name}, daemon={thread.daemon}, id={thread.ident}')

from threading import main_thread
# get the main thread
thread = main_thread()
# report properties for the main thread
print(f'name={thread.name}, daemon={thread.daemon}, id={thread.ident}')
```

# Thread方法

### threading.active_count()

可以通过`threading.active_count()`方法来获得当前线程的数量。

```python
from threading import active_count
# get the number of active threads
count = active_count()
# report the number of active threads
print(count)
```

### **threading.current_thread()**

获得当前线程

```python
from threading import Thread
from threading import current_thread
 
# function to get the current thread
def task():
    # get the current thread
    thread = current_thread()
    # report the name
    print(thread.name)
 
# create a thread
thread = Thread(target=task)
# start the thread
thread.start()
# wait for the thread to exit
thread.join()
```

### **threading.get_ident()**

获得当前线程的id

```python
from threading import get_ident
# get the id for the current thread
identifier = get_ident()
# report the thread id
print(identifier)
```

### **threading.get_native_id()**

获得当前线程的native id

```python
from threading import get_native_id
# get the native id for the current thread
identifier = get_native_id()
# report the thread id
print(identifier)
```

### **threading.enumerate()**

获得当前活跃的线程的列表。

```python
import threading
# get a list of all active threads
threads = threading.enumerate()
# report the name of all active threads
for thread in threads:
    print(thread.name)
```

# 线程异常处理

线程中出现的异常会终止线程的运行。

```python
from time import sleep
from threading import Thread
 
# target function that raises an exception
def work():
    print('Working...')
    sleep(1)
    # rise an exception
    raise Exception('Something bad happened')
 
# create a thread
thread = Thread(target=work)
# run the thread
thread.start()
# wait for the thread to finish
thread.join()
# continue on
print('Continuing on...')
```

线程阻塞1秒后raise了一个异常，终止了当前线程。需要注意的是，线程的失败不会影响main线程的运行。

```
Working...
Exception in thread Thread-1:
Traceback (most recent call last):
  ...
  exception_unhandled.py", line 11, in work
    raise Exception('Something bad happened')
Exception: Something bad happened
Continuing on...
```

### 异常hook

我们可以通过Hook函数来定义如何处理异常和错误。

首先，我们定义一个函数，其中的参数是**ExceptHookArgs** 类的对象，包含了线程和异常的细节。然后我们将这个函数赋给线程的`excepthook `属性。

```python
from time import sleep
import threading
 
# target function that raises an exception
def work():
    print('Working...')
    sleep(1)
    # rise an exception
    raise Exception('Something bad happened')
 
# custom exception hook
def custom_hook(args):
    # report the failure
    print(f'Thread failed: {args.exc_value}')
 
# set the exception hook
threading.excepthook = custom_hook
# create a thread
thread = threading.Thread(target=work)
# run the thread
thread.start()
# wait for the thread to finish
thread.join()
# continue on
print('Continuing on...')
```

当我们运行上述代码，发生异常之后，会按照`custom_hook()`方法来处理。

```
Working...
Thread failed: Something bad happened
Continuing on...
```

# python线程的限制和使用场景

python的解释器是CPython，Cpython解释器不允许多个线程同时运行。这是由于在解释器中有一个互斥锁，只允许同时一个线程在Python虚拟机中执行Python二进制码。这个互斥锁被称为GIL(Global Interpreter Lock)。

这也就是说，尽管我们可以写并行的代码，并且在多核的机器上跑这个代码，我们可能还是无法真的并行地运行代码。但是也有例外情况，比如说线程正在进行IO，或者正在进行计算密集型地代码，如Hash函数。

### 在阻塞IO的时候用线程

IO任务包括设备、文件或者网络连接的读写，这类操作包括input和output，这类操作的速度取决于硬件条件，相对于CPU操作是相对慢的。而IO操作需要在操作系统里进行的操作，往往需要内核去等待，如果你的程序主要依赖于CPU，那么等待IO会导致你的程序运行缓慢。

一个正在进行IO操作的线程会暂时阻塞，当前线程被阻塞之后，操作系统会启动别的线程，这被称为上下文切换。同时，GIL也会在IO阻塞时释放，允许别的线程开始执行。

常见的IO操作包括

* 硬盘文件的读写
* stdin，stdout，stderr的读写
* 网络IO（下载上传文件，读取字节）
* 请求数据库 

等等。

### 使用外部C代码时

我们在使用某些python函数的时候会使用到一些第三方c语言库，这些库的使用会释放GIL。

例如，`hash`模块在调用`hash.update()`函数时，或者`NumPy`库管理数据数组的时候。

# python线程常见问题

### 怎么终止一个线程？

Python没有终止线程的API，但是我们可以通过**threading.Event**这个线程安全的boolean变量来实现。这个变量是线程共享的，我们可以通过`is_set()`方法在线程中判断`event`变量值，如果值是`True`，就退出线程循环。在main线程中，可以通过`set()`方法来设置变量值。

```python
from time import sleep
from threading import Thread
from threading import Event
 
# custom task function
def task(event):
    # execute a task in a loop
    for i in range(5):
        # block for a moment
        sleep(1)
        # check for stop
        if event.is_set():
            break
        # report a message
        print('Worker thread running...')
    print('Worker closing down')
 
# create the event
event = Event()
# create and configure a new thread
thread = Thread(target=task, args=(event,))
# start the new thread
thread.start()
# block for a while
sleep(3)
# stop the worker thread
print('Main stopping thread')
event.set()
# wait for the new thread to finish
thread.join()
```

以上示例中，在线程函数中的循环中，我们判断event变量值，如果是True，就退出循环，从而退出线程函数。我们在main线程中设置event变量的值。

### 怎么等待线程结束？

我们可以通过`join()`来等待线程终止，这会阻塞当前线程直到join的线程返回（完成了目标方法或者发生了错误或异常）。

### 怎么重启一个线程？

python线程无法被重启。如果一个线程终止了，调用`start()`方法会抛出异常。

### 怎么获取线程返回值？

Python线程没有直接的方法去获取另一个线程的返回值，我们可以通过间接的方法：

1. 使用` queue.Queue`在线程中共享结果
2. 使用全局变量在线程中共享结果
