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
