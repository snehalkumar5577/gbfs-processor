import os
from typing import Type

class Config:
    MONGODB_HOST: str = os.getenv("MONGODB_HOST", "mongo")
    MONGODB_PORT: str = "27017"
    MONGODB_DB_NAME: str = "gbfs_database"
    COLLECTION_NAME: str = "gbfs_collection"
    MONGODB_USER: str = os.getenv("MONGODB_USERNAME", "root")
    MONGODB_PASSWORD: str = os.getenv("MONGODB_PASSWORD", "password")
    MONGODB_URI: str = f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DB_NAME}?authSource=admin"

class DevelopmentConfig(Config):
    LOG_LEVEL: str = "DEBUG"

class ProductionConfig(Config):
    LOG_LEVEL: str = "INFO"

def get_config() -> Type[Config]:
    environment = os.getenv("ENVIRONMENT", "prod").lower()
    if environment == "dev":
        return DevelopmentConfig
    return ProductionConfig