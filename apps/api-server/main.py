from datetime import datetime, timezone
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

class StationAvailability(BaseModel):
    station_id: str
    provider: str
    available_bikes: int
    timestamp: datetime

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

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

# Endpoint for bike summary by provider
@app.get("/api/providers/summary", response_model=List[ProviderSummary])
async def get_bike_summary():
    """Aggregates and returns the number of available bikes by provider."""
    pipeline = [
        {"$group": {"_id": "$provider", "available_bikes": {"$sum": "$available_bikes"}}},
    ]
    summary = await client.collection.aggregate(pipeline).to_list(100)
    
    return [ProviderSummary(provider=item["_id"], available_bikes=item["available_bikes"]) for item in summary]

# Endpoint for station availability
@app.get("/api/stations/availability")
async def get_station_availability(provider: str = None, station_id: str = None):
    """Returns the latest availability data for all stations."""
    query = {}
    if provider:
        query["provider"] = provider
    if station_id:
        query["station_id"] = station_id

    stations = await client.collection.find(query).to_list(100)
    # Convert it to json serializable format
    return [StationAvailability(**station) for station in stations]


# Endpoint for station availability time series
@app.get("/api/stations/timeseries", response_model=List[StationAvailability])
# example usage: /api/stations/timeseries?start_date=2021-01-01T00:00:00&end_date=2021-01-02T00:00:00
async def get_station_timeseries(station_id: str = None, provider: str = None, start_date: datetime = None, end_date: datetime = None):
    """Returns the time series data of bike availability for the specified station or provider."""
    
    query = {}
    if provider:
        query["provider"] = provider
    if station_id:
        query["station_id"] = station_id
    if start_date and end_date:
        query["timestamp"] = {"$gte": start_date, "$lt": end_date}
    
    stations = await client.collection.find(query).to_list(100)
    return [StationAvailability(**station) for station in stations]

# Endpoint to get all providers
@app.get("/api/providers")
async def get_providers():
    """Returns the list of all providers."""
    pipeline = [
        {"$group": {"_id": "$provider"}},
    ]
    providers = await client.collection.aggregate(pipeline).to_list(100)
    return [provider["_id"] for provider in providers]