import os
from typing import Type

class Config:
    MONGO_URI: str = os.getenv("MONGODB_URI", "mongodb://mongo:27017")
    MONGO_USERNAME: str = os.getenv("MONGODB_USERNAME", "root")
    MONGO_PASSWORD: str = os.getenv("MONGODB_PASSWORD", "password")
    DB_NAME: str = os.getenv("DB_NAME", "gbfs_database")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "gbfs_collection")
    PROVIDERS: dict = {
        "Careem BIKE": "https://dubai.publicbikesystem.net/customer/gbfs/v2/gbfs.json",
        "Blue-bike": "https://api.delijn.be/gbfs/gbfs.json",
        "Zenica": "https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_bz/gbfs.json"
    }

class DevelopmentConfig(Config):
    LOG_LEVEL: str = "DEBUG"

class ProductionConfig(Config):
    LOG_LEVEL: str = "INFO"

def get_config() -> Type[Config]:
    environment = os.getenv("ENVIRONMENT", "prod").lower()
    if environment == "dev":
        return DevelopmentConfig
    return ProductionConfig