import os
from typing import Optional

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
