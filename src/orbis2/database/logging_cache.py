import logging.config

from cachetools import TTLCache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cachetools")


class LoggingCache(TTLCache):
    def __getitem__(self, key):
        try:
            value = super().__getitem__(key)
            logging.info(f"Cache hit for key: {key}")
            return value
        except KeyError:
            logging.info(f"Cache miss for key: {key}")
            raise


# create cache with a maximum size of 100 and a time-to-live of 600 seconds
cache = LoggingCache(maxsize=100, ttl=600)
