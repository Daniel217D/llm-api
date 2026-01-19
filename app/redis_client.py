import hashlib
import json
import os
from collections.abc import Callable
from typing import Any

import redis

# Redis configuration
redis_host: str = os.getenv("REDIS_HOST", "redis")
redis_port: int = int(os.getenv("REDIS_PORT", "6379"))
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)


def get_from_redis(key: Any) -> str | None:
    """
    Get value from Redis by key.

    Args:
            key: Redis key (any JSON-serializable object or string)

    Returns:
            Value from Redis or None if key doesn't exist
    """
    try:
        return redis_client.get(get_cache_key(key))
    except redis.RedisError:
        return None


def set_to_redis(key: Any, value: str, expire: int | None = None) -> bool:
    """
    Set value to Redis with optional expiration.

    Args:
            key: Redis key (any JSON-serializable object or string)
            value: Value to store
            expire: Optional expiration time in seconds

    Returns:
            True if successful, False otherwise
    """
    try:
        cache_key = get_cache_key(key)
        if expire:
            redis_client.setex(cache_key, expire, value)
        else:
            redis_client.set(cache_key, value)
        return True
    except redis.RedisError:
        return False


def get_cache_key(key: Any) -> str:
    """
    Generate cache key from any JSON-serializable object.

    Args:
            key: Cache key (any JSON-serializable object)

    Returns:
            Cache key string
    """
    key_json = json.dumps(key, sort_keys=True, ensure_ascii=False)
    key_hash = hashlib.md5(key_json.encode("utf-8")).hexdigest()
    return f"cache:{key_hash}"


def remember(key: Any, callback: Callable[[], str], expire: int = 1800) -> str:
    """
    Get value from cache or execute callback and cache the result.

    Args:
            key: Cache key (any JSON-serializable object)
            callback: Function to call if cache miss
            expire: Cache expiration time in seconds (default: 1800)

    Returns:
            Cached value or result from callback
    """
    # Try to get from cache
    cached_value = get_from_redis(key)
    if cached_value is not None:
        return cached_value

    # Cache miss - execute callback and cache result
    value = callback()
    set_to_redis(key, value, expire=expire)
    return value


def service_id(fn) -> str:
    """
    Get a unique identifier for a function.

    Args:
        fn: Function to get identifier for

    Returns:
        Unique identifier string
    """
    return f"{fn.__module__}:{fn.__qualname__}"
