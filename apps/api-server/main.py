from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import os


# MongoDB connection
MONGODB_HOST = os.getenv("MONGODB_HOST", "mongo")
MONGODB_PORT = "27017"
MONGODB_DB_NAME = "gbfs_database"
COLLECTION_NAME = "gbfs_collection"
MONGODB_USER = os.getenv("MONGODB_USERNAME", "root")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "password")

MONGODB_URI = f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DB_NAME}?authSource=admin"


# Initialize FastAPI and MongoDB client
app = FastAPI()
client = AsyncIOMotorClient(MONGODB_URI)
db = client[MONGODB_DB_NAME]
collection = db[COLLECTION_NAME]

# Pydantic Model for the response
class ProviderSummary(BaseModel):
    provider: str
    total_bikes: int

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Endpoint for bike summary by provider
@app.get("/api/stations/summary", response_model=List[ProviderSummary])
async def get_bike_summary():
    """Aggregates and returns the number of available bikes by provider."""
    pipeline = [
        {"$group": {"_id": "$provider", "total_bikes": {"$sum": "$num_bikes_available"}}}
    ]
    summary = await collection.aggregate(pipeline).to_list(100)
    return [{"provider": item["_id"], "total_bikes": item["total_bikes"]} for item in summary]

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}