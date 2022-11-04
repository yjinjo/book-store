# ex02_scraping_openapi.py


import aiohttp
import asyncio
from config import get_secret


async def fetch(session, url):
    headers = {
        "X-Naver-Client-id": get_secret("NAVER_API_ID"),
        "X-Naver-Client-Secret": get_secret("NAVER_API_SECRET"),
    }

    async with session.get(url, headers=headers) as response:
        result = await response.json()  # JSON 객체를 가져 오므로 text가 아니라 json()
        items = result["items"]
        images = [item["link"] for item in items]
        print(images)


async def main():
    BASE_URL = "https://openapi.naver.com/v1/search/image"
    keyword = "cat"  # 검색어

    urls = [f"{BASE_URL}?query={keyword}&display=20&start={i}" for i in range(1, 10)]

    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetch(session, url) for url in urls])


if __name__ == "__main__":
    asyncio.run(main())
