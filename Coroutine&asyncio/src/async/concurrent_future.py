import asyncio
import time


def func():
    time.sleep(1)
    return "result"


async def main():
    loop = asyncio.get_running_loop()
    fut = loop.run_in_executor(None, func)
    res = await fut
    print("default thread pool", res)


if __name__ == '__main__':
    asyncio.run(main())
