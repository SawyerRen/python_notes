import aioredis
import asyncio


async def func(address, pwd):
    print("start process")

    redis = await aioredis.create_redis(address, pwd)

    await redis.set('car', 1)

    redis.close()

    await redis.wait_closed()

    print("end")
