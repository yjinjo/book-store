# ex07_coroutine.py

import asyncio


async def hello_world():
    await print("hello world")
    return 123


if __name__ == "__main__":
    asyncio.run(hello_world())
