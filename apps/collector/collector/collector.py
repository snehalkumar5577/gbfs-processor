from config import config as conf
from . import logger
from . import fetcher

def main():
    log = logger.get_logger()
    config = conf.get_config()
    
    log.info("Starting data collection")

    for provider, url in config.PROVIDERS.items():
        fetcher.fetch_and_store_data(provider, url)

    log.info("Data collection completed")
