import requests
import aiohttp
import asyncio


async def fetch(session, url):
    async with session.get(url) as response:
        content = await response.content.read()
        file_name = url.rsplit("_")[-1]
        with open(file_name, 'wb') as file_obj:
            file_obj.write(content)


async def main():
    async with aiohttp.ClientSession() as session:
        url_list = []
        tasks = [asyncio.create_task(fetch(session, url)) for url in url_list]
        await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.run(main())
