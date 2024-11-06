import os
from typing import Type
import json

class Config:
    MONGO_URI: str = os.getenv("MONGODB_URI", "mongodb://mongo:27017")
    MONGO_USERNAME: str = os.getenv("MONGODB_USERNAME", "root")
    MONGO_PASSWORD: str = os.getenv("MONGODB_PASSWORD", "password")
    DB_NAME: str = os.getenv("DB_NAME", "gbfs_database")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "gbfs_collection")
    # Default providers
    default_providers = {
        "Careem BIKE": "https://dubai.publicbikesystem.net/customer/gbfs/v2/gbfs.json",
        "Blue-bike": "https://api.delijn.be/gbfs/gbfs.json",
        "Zenica": "https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_bz/gbfs.json"
    }
    # Override providers with environment variable if available
    providers_json = os.getenv("PROVIDERS_JSON", json.dumps(default_providers))
    try:
        PROVIDERS = json.loads(providers_json)
    except json.JSONDecodeError:
        PROVIDERS = default_providers

class DevelopmentConfig(Config):
    LOG_LEVEL: str = "DEBUG"

class ProductionConfig(Config):
    LOG_LEVEL: str = "INFO"

def get_config() -> Type[Config]:
    environment = os.getenv("ENVIRONMENT", "prod").lower()
    if environment == "dev":
        return DevelopmentConfig
    return ProductionConfig