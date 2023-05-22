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
