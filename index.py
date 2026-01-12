from typing import Any, Optional
from dotenv import load_dotenv

from app.service import chat

load_dotenv()

from fastapi import FastAPI, Query, HTTPException, Depends, Body

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
    description="Accepts a `payload` query parameter and sends it to GigaChat"
)
async def _(
    payload: Optional[str] = Query(
        default=None,
        description="Text message to send to GigaChat"
    ),
    _: None = Depends(verify_token),
) -> Any:
    if not payload:
        raise HTTPException(
            status_code=422,
            detail="The 'payload' query parameter is required"
        )

    return chat(payload)

@app.post(
    "/gigachat/chat",
    summary="Send a message to GigaChat",
    description="Accepts a `payload` in body and sends it to GigaChat"
)
async def _(
    payload: Optional[str] = Body(
        default=None,
        description="Text message to send to GigaChat",
        media_type="application/json",
    ),
    _: None = Depends(verify_token),
) -> Any:
    if not payload:
        raise HTTPException(
            status_code=422,
            detail="The 'payload' query parameter is required"
        )

    return chat(payload)
