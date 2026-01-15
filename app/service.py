from enum import Enum

from gigachat import GigaChat

from app.redis_client import remember, service_id, set_to_redis
from app.token_manager import get_or_refresh_token


class GigaChatModel(str, Enum):
    GIGACHAT = "GigaChat"
    GIGACHAT_PRO = "GigaChat-Pro"
    GIGACHAT_MAX = "GigaChat-Max"


def chat(payload: str, model: GigaChatModel = GigaChatModel.GIGACHAT, no_cache: bool = False, reset_cache: bool = False) -> str:
    """
    Send a message to GigaChat and get response.
    
    Args:
        payload: Text message to send to GigaChat
        model: GigaChat model to use (default: GigaChat)
        no_cache: If True, skip cache and make a fresh request without caching
        reset_cache: If True, skip cache check but save result to cache
    
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
    
    # Cache key based on payload and model
    cache_key_obj = {
        "service": service_id(chat),
        "model": model.value,
        "payload": payload
    }
    
    # If no_cache, skip cache completely
    if no_cache:
        return get_response()
    
    # If reset_cache, skip cache check but save result
    if reset_cache:
        response_content = get_response()
        set_to_redis(cache_key_obj, response_content, expire=1800)
        return response_content
    
    # Normal caching behavior
    return remember(cache_key_obj, get_response, expire=1800)