# ex03_multi_threading.py

import requests
import time

import os
import threading

from concurrent.futures import ThreadPoolExecutor


def fetcher(params):
    session = params[0]
    url = params[1]
    print(f"{os.getpid()} process | {threading.get_ident()} url: {url}")
    with session.get(url) as response:
        return response.text


def main():
    urls = ["https://www.google.com", "https://www.apple.com"] * 10

    executor = ThreadPoolExecutor(max_workers=10)  # Multi Thread

    with requests.Session() as session:
        params = [(session, url) for url in urls]
        results = list(executor.map(fetcher, params))
        # print(results)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)
