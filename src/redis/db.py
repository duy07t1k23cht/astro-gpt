import os
import redis

from dotenv import load_dotenv

from src.views.custom_logger import logger

load_dotenv()

database = None
redis_url = os.environ.get("REDIS_URL")
if redis_url is not None:
    database = redis.from_url(redis_url)
else:
    logger.w("Cannot init redis database")
