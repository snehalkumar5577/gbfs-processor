import pytest
from unittest.mock import patch, MagicMock
from .database import MongoDBClient, get_mongo_client
from config.config import Config

@pytest.fixture
def mock_config():
    class MockConfig:
        MONGO_URI = "mongodb://localhost:27017"
        MONGO_USERNAME = "user"
        MONGO_PASSWORD = "password"
        DB_NAME = "test_db"
        COLLECTION_NAME = "test_collection"
    return MockConfig

@pytest.fixture
def mock_mongo_client():
    with patch('collector.database.MongoClient') as mock_client:
        yield mock_client

@pytest.fixture
def mongo_db_client(mock_config, mock_mongo_client):
    return get_mongo_client(mock_config)

def test_get_mongo_client(mock_config):
    client = get_mongo_client(mock_config)
    assert isinstance(client, MongoDBClient)
    assert client.db.name == mock_config.DB_NAME
    assert client.collection.name == mock_config.COLLECTION_NAME