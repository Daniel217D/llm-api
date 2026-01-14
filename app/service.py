from enum import Enum

from gigachat import GigaChat

from app.token_manager import get_or_refresh_token


class GigaChatModel(str, Enum):
    GIGACHAT = "GigaChat"
    GIGACHAT_PRO = "GigaChat-Pro"
    GIGACHAT_MAX = "GigaChat-Max"


def chat(payload: str, model: GigaChatModel = GigaChatModel.GIGACHAT) -> str:
    """
    Send a message to GigaChat and get response.
    
    Args:
        payload: Text message to send to GigaChat
        model: GigaChat model to use (default: GigaChat)
    
    Returns:
        Response content from GigaChat
    """
    with GigaChat(
        access_token=get_or_refresh_token(),
        verify_ssl_certs=False,
        model=model.value
    ) as giga:
        response = giga.chat(payload)

    return response.choices[0].message.content