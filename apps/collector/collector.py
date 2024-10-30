import os
import requests
from pymongo import MongoClient
from datetime import datetime

config = {
    "MONGO_URI": os.getenv("MONGODB_URI", "mongodb://mongo:27017"),
    "MONGO_USERNAME": os.getenv("MONGODB_USERNAME", "root"),
    "MONGO_PASSWORD": os.getenv("MONGODB_PASSWORD", "password"),
    "DB_NAME": "gbfs_database",
    "COLLECTION_NAME": "gbfs_collection",
    "PROVIDERS": {
        "Careem BIKE" : "https://dubai.publicbikesystem.net/customer/gbfs/v2/gbfs.json",
        "Blue-bike" : "https://api.delijn.be/gbfs/gbfs.json",
        "Zenica" : "https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_bz/gbfs.json"
    }
}

# create mongo client using uri, username and password
client = MongoClient(config["MONGO_URI"], username=config["MONGO_USERNAME"], password=config["MONGO_PASSWORD"])
db = client[config["DB_NAME"]]
collection = db[config["COLLECTION_NAME"]]

def fetch_data(url):
    """Fetch data from the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

def extract_station_info(provider_name, provider_url):
    gbfs_data = fetch_data(provider_url)
    
    if gbfs_data is None:
        return
    
    feeds = gbfs_data.get("data", {}).get("en", {}).get("feeds", [])
    station_info_url = None
    
    for feed in feeds:
        if feed["name"] == "station_status":
            station_info_url = feed["url"]
            break

    if station_info_url is None:
        print("Station information URL not found.")
        return

    print(f"Fetching station information from {station_info_url}...")
    station_data = fetch_data(station_info_url)

    if station_data is None:
        return

    stations = station_data.get("data", {}).get("stations", [])

    timestamp = datetime.utcnow()
    
    for station in stations:
        record = {
            "provider": provider_name,
            "station_id": station["station_id"],
            "num_bikes_available": station["num_bikes_available"],
            "timestamp": timestamp
        }
        collection.insert_one(record)
        print(f"Inserted record for station_id {station['station_id']}.")

def main():
    for provider_name, provider_url in config["PROVIDERS"].items():
        extract_station_info(provider_name, provider_url)

if __name__ == "__main__":
    main()