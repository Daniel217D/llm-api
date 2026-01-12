from gigachat import GigaChat

from app.token_manager import get_or_refresh_token


def chat(payload: str) -> str:
    with GigaChat(
        access_token=get_or_refresh_token(),
        verify_ssl_certs=False,
        model="GigaChat"
    ) as giga:
        response = giga.chat(payload)

    return response.choices[0].message.content