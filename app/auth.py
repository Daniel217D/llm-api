import base64
import os

from fastapi import Header, HTTPException

# Get API token from environment
API_TOKEN = os.getenv("APP_API_KEY", "")
API_BASIC_USER = os.getenv("APP_BASIC_USER", "")
API_BASIC_PASSWORD = os.getenv("APP_BASIC_PASSWORD", "")


async def verify_token(authorization: str | None = Header(None)) -> None:
    """
    Verify API token from Authorization header.

    Args:
            authorization: Authorization header value (Bearer <token>)

    Raises:
            HTTPException: If token is missing or invalid
    """
    if not API_TOKEN:
        raise HTTPException(
            status_code=500, detail="APP_API_KEY is not configured"
        ) from None

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header is required",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    parts = authorization.split(maxsplit=1)
    if len(parts) != 2:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer, Basic"},
        ) from None

    scheme, credentials = parts[0].lower(), parts[1]

    if scheme == "bearer":
        if credentials != API_TOKEN:
            raise HTTPException(
                status_code=401,
                detail="Invalid API token",
                headers={"WWW-Authenticate": "Bearer"},
            ) from None

    elif scheme == "basic":
        try:
            decoded = base64.b64decode(credentials).decode("utf-8")
            username, password = decoded.split(":", 1)
        except Exception:
            raise HTTPException(
                status_code=401,
                detail="Invalid basic authorization credentials",
                headers={"WWW-Authenticate": "Basic"},
            ) from None

        if username != API_BASIC_USER or password != API_BASIC_PASSWORD:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Basic"},
            ) from None

    else:
        raise HTTPException(
            status_code=401,
            detail="Unsupported authorization scheme",
            headers={"WWW-Authenticate": "Bearer, Basic"},
        ) from None
