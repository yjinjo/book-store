# ex03_image_downloader.py

from config import get_secret
import os
import aiohttp
import asyncio
import aiofiles


async def img_downloader(session, img):
    # 매개변수 img 형식은 'https://i.pinimg.com/736x/e7/77/47/e77747c28f1fe2f77d5f141b18a6cdf4.jpg' 와 같다.

    img_name = img.split("/")[-1].split("?")[0]  # ~.jpg

    try:
        os.mkdir("./images")  # 현재 루트에 images 디렉터리를 만듦
    except FileExistsError:  # 만약 이미 존재하는 디렉터리라면 에러가 나게 만듦. 우선은 pass
        pass

    async with session.get(img) as response:
        if response.status == 200:
            async with aiofiles.open(f"./images/{img_name}", mode="wb") as file:
                # 이미지 데이터를 읽은 다음에 images 디렉터리에 img_name 으로 이미지 저장
                img_data = await response.read()
                await file.write(img_data)


async def fetch(session, url):
    headers = {
        "X-Naver-Client-id": get_secret("NAVER_API_ID"),
        "X-Naver-Client-Secret": get_secret("NAVER_API_SECRET"),
    }

    async with session.get(url, headers=headers) as response:
        result = await response.json()
        items = result["items"]
        images = [item["link"] for item in items]

        await asyncio.gather(*[img_downloader(session, img) for img in images])


async def main():
    BASE_URL = "https://openapi.naver.com/v1/search/image"
    keyword = "cat"

    urls = [f"{BASE_URL}?query={keyword}&display=20&start={i * 20 + 1}" for i in range(10)]

    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetch(session, url) for url in urls])


if __name__ == "__main__":
    asyncio.run(main())
