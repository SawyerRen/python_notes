import asyncio


# async def func():
#     print(1)
#     response = await asyncio.sleep(2)
#     print("2", response)

async def others():
    print("start")
    await asyncio.sleep(2)
    print("end")
    return 1


async def func():
    print("start func")
    response = await others()
    print("end func, response = ", response)


if __name__ == '__main__':
    asyncio.run(func())
