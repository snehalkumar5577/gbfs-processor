from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import database
import logger

# Initialize FastAPI and MongoDB client
app = FastAPI()
client = database.get_mongo_client()
log = logger.get_logger()

# Pydantic Model for the response
class ProviderSummary(BaseModel):
    provider: str
    available_bikes: int

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Endpoint for bike summary by provider
@app.get("/api/providers/summary", response_model=List[ProviderSummary])
async def get_bike_summary():
    """Aggregates and returns the number of available bikes by provider."""
    pipeline = [
        {"$group": {"_id": "$provider", "available_bikes": {"$sum": "$available_bikes"}}},
    ]
    summary = await client.collection.aggregate(pipeline).to_list(100)
    
    return [{"provider": item["_id"], "available_bikes": item["available_bikes"]} for item in summary]


# Health check endpoint
@app.get("/health")
async def health_check():
    """Checks if the API server is up and running."""
    return {"status": "ok"}


# Readiness check endpoint
@app.get("/ready")
async def readiness_check():
    """Checks if the MongoDB connection is up and running."""
    try:
        client.db.command("ping")
        return {"status": "ok"}
    except Exception as e:
        log.error(f"Error connecting to MongoDB: {e}")
        return {"status": "down"}