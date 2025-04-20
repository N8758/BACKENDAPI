import redis
from .config import REDIS_URL

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def get_cache(key: str):
    return redis_client.get(key)

def set_cache(key: str, value: str):
    redis_client.set(key, value, ex=3600)  # cache for 1 hour
