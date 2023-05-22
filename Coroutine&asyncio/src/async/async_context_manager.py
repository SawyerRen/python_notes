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
