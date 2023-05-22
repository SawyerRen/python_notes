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
