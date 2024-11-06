import logging
import config as conf

def configure_logger(config: conf.Config) -> logging.Logger:
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger('collector')
    return logger

# getter
def get_logger() -> logging.Logger:
    return configure_logger(conf.get_config())