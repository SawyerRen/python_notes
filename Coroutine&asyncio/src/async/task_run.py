import asyncio


async def func():
    await asyncio.sleep(1)
    print("async func")


async def main():
    task = asyncio.create_task(func())
    await asyncio.sleep(0)


if __name__ == '__main__':
    asyncio.run(main())
