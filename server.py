# server.py

import uvicorn

if __name__ == "__main__":
    # 모든 사용자가 접속할 수 있도록 host는 0.0.0.0으로, port는 80으로 바꾼다.
    # 80번 포트가 웹에서 기본적으로 작동하는 인터넷 port이다.
    uvicorn.run("app.main:app", host="0.0.0.0", port=80, reload=False)
