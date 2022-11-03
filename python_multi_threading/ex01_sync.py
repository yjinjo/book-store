# ex01_single_threading.py

import requests
import time

# 파이썬 안에 내장되어 있는 패키지들
import os
import threading


def fetcher(session, url):
    print(f"{os.getpid()} process | {threading.get_ident()} url: {url}")
    with session.get(url) as response:
        return response.text


def main():
    urls = ["https://www.google.com", "https://www.apple.com"] * 10

    with requests.Session() as session:
        result = [fetcher(session, url) for url in urls]
        # print(result)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)
