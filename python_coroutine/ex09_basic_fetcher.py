# ex09_basic_fetcher.py
import requests
import time


def fetcher(session, url):
    with session.get(url) as response:
        return response.text


def main():
    urls = ["https://www.naver.com", "https://www.google.com", "https://www.instagram.com"] * 10

    # # 1. 먼저 Session을 연다.
    # session = requests.Session()

    # # 2. Session을 통해 해당 url을 get 으로 가져온다.
    # session.get(url)

    # # 3. 열려있는 session을 닫아줘야 하는데, with 키워드를 통해서 닫을 수 있다.
    # session.close()

    # 위의 3가지 step을 아래의 with 구문 하나로 바꿀 수 있다. (with 구문은 세션을 자동으로 닫아준다.)
    # with requests.Session() as session:
    #     session.get(url)

    with requests.Session() as session:
        # 여기서 fetcher의 의미는 해당하는 Session에 url을 보내서 데이터를 가져온다.
        result = [fetcher(session, url) for url in urls]
        print(result)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)
