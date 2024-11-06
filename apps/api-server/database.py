from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict, Any
import config as conf
import logger

log = logger.get_logger()

class MongoDBClient:
    def __init__(self, uri: str, username: str, password: str, db_name: str, collection_name: str):
        self.client = AsyncIOMotorClient(uri, username=username, password=password)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_data(self, data: Dict[str, Any]) -> None:
        try:
            self.collection.insert_one(data)
            log.info(f"Data inserted for provider: {data['provider']}")
        except Exception as e:
            log.error(f"Error inserting data for provider: {data['provider']}, Error: {e}")

def get_mongo_client() -> MongoDBClient:
    config = conf.get_config()
    return MongoDBClient(
        uri=config.MONGODB_URI,
        username=config.MONGODB_USER,
        password=config.MONGODB_PASSWORD,
        db_name=config.MONGODB_DB_NAME,
        collection_name=config.COLLECTION_NAME
    )