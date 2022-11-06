# app/book_scraper.py

from app.config import get_secret
import aiohttp
import asyncio


class NaverBookScraper:

    NAVER_API_BOOK = "https://openapi.naver.com/v1/search/book"
    NAVER_API_ID = get_secret("NAVER_API_ID")
    NAVER_API_SECRET = get_secret("NAVER_API_SECRET")

    @staticmethod
    async def fetch(session, url, headers):
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                return result["items"]

    def unit_url(self, keyword, start):
        return {
            "url": f"{self.NAVER_API_BOOK}?query={keyword}&display=10&start={start}",
            "headers": {
                "X-Naver-Client-Id": self.NAVER_API_ID,
                "X-Naver-Client-Secret": self.NAVER_API_SECRET,
            },
        }

    async def search(self, keyword, total_page):
        # 첫 번째 페이지에서는 1 부터 10 까지의 데이터를 보여주고,
        # 두 번째 페이지에서는 11 부터 20 까지의 데이터를 보여줄 것이다, ...
        apis = [self.unit_url(keyword, i * 10 + 1) for i in range(total_page)]
        async with aiohttp.ClientSession() as session:
            all_data = await asyncio.gather(
                *[NaverBookScraper().fetch(session, api["url"], api["headers"]) for api in apis]
            )
            # [ [한 페이지에 데이터들 10개], [한 페이지에 데이터 10개], ... ] -->
            # [ 데이터 30개 ]
            result = []
            for data in all_data:
                if data:
                    for book in data:
                        result.append(book)

            return result

    def run(self, keyword, total_page):
        # asyncio의 run 같은 경우, awaitable한 객체가 아니므로 async def 와 같은 것이 필요 없다. (단순히 코루틴 함수를 실행함)
        return asyncio.run(self.search(keyword, total_page))


if __name__ == "__main__":
    scraper = NaverBookScraper()
