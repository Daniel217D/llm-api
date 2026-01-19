from typing import Any

from fastapi import Body, Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

import bootstrap  # noqa: F401
from app.auth import verify_token
from app.config import validate_environment_variables
from app.service import GigaChatModel, chat

validate_environment_variables()

app = FastAPI()


def validate_model(model: str | None = Query(default=None)) -> GigaChatModel:
    if not model:
        return GigaChatModel.GIGACHAT

    try:
        return GigaChatModel(model)
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid model '{model}'. Available models: {', '.join([m.value for m in GigaChatModel])}",
        ) from None


def validate_payload_from_query(
    payload: str | None = Query(
        default=None, description="Text message to send to GigaChat"
    ),
) -> str:
    if not payload:
        raise HTTPException(
            status_code=422, detail="The 'payload' query parameter is required"
        ) from None
    return payload


def validate_payload_from_body(
    payload: str | None = Body(
        default=None,
        description="Text message to send to GigaChat",
        media_type="text/plain",
    ),
) -> str:
    if not payload:
        raise HTTPException(status_code=422, detail="The body is required") from None
    return payload


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", summary="Nothing here", description="Temporary stub")
async def root() -> dict[str, str]:
    return {"status": "ok", "message": "Home endpoint stub"}


@app.get(
    "/gigachat/chat",
    summary="Send a message to GigaChat",
    description="Accepts a `payload` query parameter and sends it to GigaChat",
)
async def _(
    payload: str = Depends(validate_payload_from_query),
    model: GigaChatModel = Depends(validate_model),
    no_cache: int | None = Query(default=None, description="Set to 1 to skip cache"),
    reset_cache: int | None = Query(
        default=None, description="Set to 1 to reset cache"
    ),
    _: None = Depends(verify_token),
) -> Any:
    return chat(
        payload, model, no_cache=(no_cache == 1), reset_cache=(reset_cache == 1)
    )


@app.post(
    "/gigachat/chat",
    summary="Send a message to GigaChat",
    description="Accepts a message in body and sends it to GigaChat",
)
async def _(
    payload: str = Depends(validate_payload_from_body),
    model: GigaChatModel = Depends(validate_model),
    no_cache: int | None = Query(default=None, description="Set to 1 to skip cache"),
    reset_cache: int | None = Query(
        default=None, description="Set to 1 to reset cache"
    ),
    _: None = Depends(verify_token),
) -> Any:
    return chat(
        payload, model, no_cache=(no_cache == 1), reset_cache=(reset_cache == 1)
    )
