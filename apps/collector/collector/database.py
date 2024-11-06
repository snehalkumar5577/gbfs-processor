from pymongo import MongoClient
from typing import Dict, Any
from config import config as conf
from . import logger

log = logger.get_logger()

class MongoDBClient:
    def __init__(self, uri: str, username: str, password: str, db_name: str, collection_name: str):
        self.client = MongoClient(uri, username=username, password=password)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_data(self, data: Dict[str, Any]) -> None:
        try:
            self.collection.insert_one(data)
            log.info(f"Data inserted for provider: {data['provider']}")
        except Exception as e:
            log.error(f"Error inserting data for provider: {data['provider']}, Error: {e}")

def get_mongo_client(config: conf.Config) -> MongoDBClient:
    return MongoDBClient(
        uri=config.MONGO_URI,
        username=config.MONGO_USERNAME,
        password=config.MONGO_PASSWORD,
        db_name=config.DB_NAME,
        collection_name=config.COLLECTION_NAME
    )