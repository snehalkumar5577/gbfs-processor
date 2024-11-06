from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import database

# Initialize FastAPI and MongoDB client
app = FastAPI()
client = database.get_mongo_client()

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
    summary = await client.collection.aggregate(pipeline).to_list(100)
    
    return [{"provider": item["_id"], "total_bikes": item["total_bikes"]} for item in summary]

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}