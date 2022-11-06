# app/main.py

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pathlib import Path

from app.models import mongodb

from app.models.book import BookModel

from app.book_scraper import NaverBookScraper


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "./index.html", {"request": request, "title": "Book Collector"}
    )


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request):
    # 1. 쿼리에서 검색어 추출
    keyword = request.query_params.get("q")
    # (예외처리)
    #   - 검색어가 없다면 사용자에게 검색을 요구 return
    if not keyword:
        context = {"request": request}
        return templates.TemplateResponse("./index.html", context=context)
    #   - 해당 검색어에 대해 수집된 데이터가 이미 DB에 존재한다면 해당 데이터를 사용자에게 보여준다. return
    #     - engine.find_one(모델, 조건)
    if await mongodb.engine.find_one(BookModel, BookModel.keyword == keyword):
        # 위의 키워드에 대해 수집된 데이터가 DB에 존재한다면 해당 데이터를 사용자에게 보여준다.
        books = await mongodb.engine.find(BookModel, BookModel.keyword == keyword)
        context = {"request": request, "keyword": keyword, "books": books}

        return templates.TemplateResponse("./index.html", context=context)

    # 2. 데이터 수집기로 해당 검색어에 대해 데이터를 수집한다.
    naver_book_scraper = NaverBookScraper()
    #  - search(keyword, total_page) 인데 우리가 한 페이지당 10개씩 오게만들었으니,
    #  - 총 100개가 올 것이다. (사용자 정의값)
    books = await naver_book_scraper.search(keyword, 10)
    book_models = []
    for book in books:
        book_model = BookModel(
            keyword=keyword,
            publisher=book["publisher"],
            discount=book["discount"],
            image=book["image"],
        )
        book_models.append(book_model)
        # engine의 save가 awaitable 객체이기 때문에 await을 붙여야한다.
        # await mongodb.engine.save(book_model)

    # 3. DB에 수집된 데이터를 저장한다.
    await mongodb.engine.save_all(book_models)

    #   - 수집된 각각의 데이터에 대해서 DB에 들어갈 모델 인스턴스를 찍는다.
    #   - 각 모델 인스턴스를 DB에 저장한다.
    context = {"request": request, "keyword": keyword, "books": books}
    return templates.TemplateResponse("./index.html", context=context)


@app.on_event("startup")
def on_app_start():
    mongodb.connect()


@app.on_event("shutdown")
def on_app_shutdown():
    mongodb.close()
