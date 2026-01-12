import os
import time

from gigachat import GigaChat

from app.redis_client import get_from_redis, set_to_redis

# Get authorization key from environment
auth_key: str = os.getenv('AUTH_KEY', '')

def get_or_refresh_token() -> str:
	"""
	Get access token from Redis or refresh it if expired/not found.
	
	Returns:
		Access token string
	"""
	token_key = 'gigachat:access_token'
	expires_at_key = 'gigachat:expires_at'
	
	# Try to get token from Redis
	access_token = get_from_redis(token_key)
	expires_at_str = get_from_redis(expires_at_key)

	
	# Check if token exists and is not expired
	if access_token and expires_at_str:
		expires_at = int(expires_at_str)
		if time.time() * 1000 < expires_at:
			return access_token
	
	# Token expired or not found, get new one
	try:
		if not auth_key:
			raise ValueError("AUTH_KEY is not set in environment variables")
		
		giga = GigaChat(credentials=auth_key, verify_ssl_certs=False)
		token_response = giga.get_token()
		
		if token_response is None:
			raise ValueError("Failed to get token from GigaChat API - received None response")
		
		access_token = token_response.access_token
		expires_at = token_response.expires_at
		
		if not access_token:
			raise ValueError("Access token is empty in response")
		
		# Store in Redis
		set_to_redis(token_key, access_token)
		set_to_redis(expires_at_key, str(expires_at))
		
		return access_token
	except Exception as e:
		print(f"Error getting GigaChat token: {e}")
		raise
