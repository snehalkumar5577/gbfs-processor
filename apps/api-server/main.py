from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import os


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# MongoDB connection
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://mongo:27017")
DB_NAME = "gbfs_database"
COLLECTION_NAME = "gbfs_collection"

# Initialize FastAPI and MongoDB client
app = FastAPI()
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Pydantic Model for the response
class ProviderSummary(BaseModel):
    provider: str
    total_bikes: int

# Endpoint for bike summary by provider
@app.get("/stations/summary", response_model=List[ProviderSummary])
async def get_bike_summary():
    """Aggregates and returns the number of available bikes by provider."""
    pipeline = [
        {"$group": {"_id": "$provider", "total_bikes": {"$sum": "$num_bikes_available"}}}
    ]
    summary = await collection.aggregate(pipeline).to_list(100)
    return [{"provider": item["_id"], "total_bikes": item["total_bikes"]} for item in summary]
