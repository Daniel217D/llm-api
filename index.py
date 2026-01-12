from typing import Any, Optional
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Query, HTTPException, Depends
from gigachat import GigaChat

from app.token_manager import get_or_refresh_token
from app.auth import verify_token
from app.config import validate_environment_variables

validate_environment_variables()

app = FastAPI()

@app.get(
    "/",
    summary="Nothing here",
    description="Temporary stub"
)
async def root() -> dict[str, str]:
    return {
        "status": "ok",
        "message": "Home endpoint stub"
    }

@app.get(
    "/gigachat/chat",
    summary="Send a message to GigaChat",
    description="Accepts a `payload` query parameter and sends it to GigaChat. Requires Bearer token authentication."
)
async def gigachat_chat(
    payload: Optional[str] = Query(
        default=None,
        description="Text message to send to GigaChat",
        example="Расскажи про Россию"
    ),
    _: None = Depends(verify_token),
) -> Any:
    if not payload:
        raise HTTPException(
            status_code=422,
            detail="The 'payload' query parameter is required"
        )

    with GigaChat(
        access_token=get_or_refresh_token(),
        verify_ssl_certs=False,
        model="GigaChat"
    ) as giga:
        response = giga.chat(payload)

    return {
        "content": response.choices[0].message.content
    }
