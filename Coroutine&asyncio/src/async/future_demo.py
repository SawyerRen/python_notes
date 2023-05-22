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
