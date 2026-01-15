from enum import Enum

from gigachat import GigaChat

from app.redis_client import remember, service_id
from app.token_manager import get_or_refresh_token


class GigaChatModel(str, Enum):
    GIGACHAT = "GigaChat"
    GIGACHAT_PRO = "GigaChat-Pro"
    GIGACHAT_MAX = "GigaChat-Max"


def chat(payload: str, model: GigaChatModel = GigaChatModel.GIGACHAT, no_cache: bool = False) -> str:
    """
    Send a message to GigaChat and get response.
    
    Args:
        payload: Text message to send to GigaChat
        model: GigaChat model to use (default: GigaChat)
        no_cache: If True, skip cache and make a fresh request
    
    Returns:
        Response content from GigaChat
    """
    def get_response() -> str:
        """Get response from GigaChat."""
        with GigaChat(
            access_token=get_or_refresh_token(),
            verify_ssl_certs=False,
            model=model.value
        ) as giga:
            response = giga.chat(payload)
        return response.choices[0].message.content
    
    # Use cache if not no_cache
    if no_cache:
        return get_response()
    
    # Cache key based on payload and model
    cache_key = {
        "service": service_id(chat),
        "model": model.value,
        "payload": payload
    }   
    
    return remember(cache_key, get_response, expire=1800)