# app/models/__init__.py

from app.config import MONGO_DB_NAME, MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine


class MongoDB:
    def __init__(self):
        self.client = None
        self.engine = None

    def connect(self):
        self.client = AsyncIOMotorClient(MONGO_URL)
        self.engine = AIOEngine(client=self.client, database=MONGO_DB_NAME)
        print("DB와 성공적으로 연결이 되었습니다.")

    def close(self):
        """서버가 죽었을 때 disconnect를 해줘야함"""
        self.client.close()


# Singleton 패턴: 단 한 번만 인스턴스를 찍으므로.
mongodb = MongoDB()
