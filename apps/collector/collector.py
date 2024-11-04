from datetime import datetime, timezone
import database as db
import config as conf
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
        if station_info:
            station_data = StationData(
                provider=provider,
                data=station_info,
                timestamp=datetime.now(timezone.utc)
            )
            mongo_client.insert_data(station_data.dict())

    log.info("Data collection completed")
if __name__ == "__main__":
    main()