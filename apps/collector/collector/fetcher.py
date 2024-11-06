import requests
from typing import Optional, Dict, Any
from . import logger
from . import models
from datetime import datetime, timezone
from . import database as db
from config import config as conf

log = logger.get_logger()

def fetch_data(url: str) -> Optional[Dict[str, Any]]:
    """Fetch data from the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        log.info(f"Data fetched from URL: {url}")
        return response.json()
    except requests.RequestException as e:
        log.error(f"Error fetching data from {url}: {e}")
        return None


def get_station_info_url(feeds: list) -> Optional[str]:
    """Extract the station info URL from the feeds."""
    for feed in feeds:
        if feed["name"] == "station_status":
            return feed["url"]
    return None

def extract_station_info(provider_name: str, provider_url: str) -> Optional[Dict[str, Any]]:
    """Extract station information for the given provider."""
    gbfs_data = fetch_data(provider_url)
    
    if gbfs_data is None:
        log.error(f"No data fetched for provider: {provider_name}")
        return None
    
    feeds = gbfs_data.get("data", {}).get("en", {}).get("feeds", [])
    station_info_url = get_station_info_url(feeds)
    
    if station_info_url is None:
        log.error(f"No station_status feed found for provider: {provider_name}")
        return None

    station_info = fetch_data(station_info_url)
    if station_info is None:
        log.error(f"Failed to fetch station info for provider: {provider_name}")
        return None

    log.info(f"Station info fetched for provider: {provider_name}")

    return station_info

def fetch_and_store_data(provider: str, url: str):
    log.info(f"Fetching data for provider: {provider}")
    station_info = extract_station_info(provider, url)
    
    if station_info is None:
        log.error(f"Failed to fetch data for provider: {provider}")
        return

    stations = station_info.get("data", {}).get("stations", [])

    for station in stations:
        station_data = models.StationData(
            provider=provider,
            station_id=station["station_id"],
            timestamp=datetime.now(timezone.utc),
            available_bikes=station["num_bikes_available"]
        )
        db.get_mongo_client(conf.get_config()).insert_data(station_data.model_dump())