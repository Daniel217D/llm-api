import os
from typing import Optional

from fastapi import HTTPException, Header

# Get API token from environment
API_TOKEN = os.getenv('APP_API_KEY', '')

async def verify_token(authorization: Optional[str] = Header(None)) -> None:
	"""
	Verify API token from Authorization header.
	
	Args:
		authorization: Authorization header value (Bearer <token>)
	
	Raises:
		HTTPException: If token is missing or invalid
	"""
	if not API_TOKEN:
		raise HTTPException(
			status_code=500,
			detail="APP_API_KEY is not configured"
		)
	
	if not authorization:
		raise HTTPException(
			status_code=401,
			detail="Authorization header is required",
			headers={"WWW-Authenticate": "Bearer"},
		)
	
	# Extract token from "Bearer <token>" format
	parts = authorization.split()
	if len(parts) != 2 or parts[0].lower() != "bearer":
		raise HTTPException(
			status_code=401,
			detail="Invalid authorization header format. Expected: Bearer <token>",
			headers={"WWW-Authenticate": "Bearer"},
		)
	
	token = parts[1]
	if token != API_TOKEN:
		raise HTTPException(
			status_code=401,
			detail="Invalid API token",
			headers={"WWW-Authenticate": "Bearer"},
		)
