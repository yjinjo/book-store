# ex02_multi_threading.py

import time
import aiohttp
import asyncio
import os
import threading


async def fetcher(session, url):
    print(f"{os.getpid()} process | {threading.get_ident()} url: {url}")
    async with session.get(url) as response:
        return await response.text()


async def main():
    urls = ["https://www.google.com", "https://www.apple.com"] * 10

    async with aiohttp.ClientSession() as session:
        result = await asyncio.gather(*[fetcher(session, url) for url in urls])
        # print(result)


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(end - start)
