import hashlib
import json
import os
from typing import Any, Callable, Optional

import redis

# Redis configuration
redis_host: str = os.getenv('REDIS_HOST', 'redis')
redis_port: int = int(os.getenv('REDIS_PORT', '6379'))
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)


def get_from_redis(key: str) -> Optional[str]:
	"""
	Get value from Redis by key.
	
	Args:
		key: Redis key
	
	Returns:
		Value from Redis or None if key doesn't exist
	"""
	try:
		return redis_client.get(key)
	except redis.RedisError:
		return None


def set_to_redis(key: str, value: str, expire: Optional[int] = None) -> bool:
	"""
	Set value to Redis with optional expiration.
	
	Args:
		key: Redis key
		value: Value to store
		expire: Optional expiration time in seconds
	
	Returns:
		True if successful, False otherwise
	"""
	try:
		if expire:
			redis_client.setex(key, expire, value)
		else:
			redis_client.set(key, value)
		return True
	except redis.RedisError:
		return False


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
	# Serialize key to JSON and create hash
	key_json = json.dumps(key, sort_keys=True, ensure_ascii=False)
	key_hash = hashlib.md5(key_json.encode('utf-8')).hexdigest()
	cache_key = f"cache:{key_hash}"
	
	# Try to get from cache
	cached_value = get_from_redis(cache_key)
	if cached_value is not None:
		return cached_value
	
	# Cache miss - execute callback and cache result
	value = callback()
	set_to_redis(cache_key, value, expire=expire)
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