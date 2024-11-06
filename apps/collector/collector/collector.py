from datetime import datetime, timezone
import database as db
from config import config as conf
import logger
from fetcher import extract_station_info
from models import StationData


def main():
    log = logger.get_logger()
    config = conf.get_config()
    mongo_client = db.get_mongo_client(config)
    
    log.info("Starting data collection")

    for provider, url in config.PROVIDERS.items():
        log.info(f"Fetching data for provider: {provider}")
        station_info = extract_station_info(provider, url)
        
        if station_info is None:
            log.error(f"Failed to fetch data for provider: {provider}")
            continue

        stations = station_info.get("data", {}).get("stations", [])

        for station in stations:
            station_data = StationData(
                provider=provider,
                station_id=station["station_id"],
                timestamp=datetime.now(timezone.utc),
                available_bikes=station["num_bikes_available"]
            )
            mongo_client.insert_data(station_data.model_dump())
        

    log.info("Data collection completed")


if __name__ == "__main__":
    main()