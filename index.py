from dotenv import load_dotenv
load_dotenv()

from typing import Any, Optional
from fastapi import FastAPI, Query, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware

from app.auth import verify_token
from app.config import validate_environment_variables
from app.service import chat, GigaChatModel

validate_environment_variables()

app = FastAPI()


def validate_model(model: Optional[str] = Query(default=None)) -> GigaChatModel:
    if not model:
        return GigaChatModel.GIGACHAT
    
    try:
        return GigaChatModel(model)
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid model '{model}'. Available models: {', '.join([m.value for m in GigaChatModel])}"
        )


def validate_payload_from_query(
    payload: Optional[str] = Query(
        default=None,
        description="Text message to send to GigaChat"
    )
) -> str:
    if not payload:
        raise HTTPException(
            status_code=422,
            detail="The 'payload' query parameter is required"
        )
    return payload


def validate_payload_from_body(
    payload: Optional[str] = Body(
        default=None,
        description="Text message to send to GigaChat",
        media_type="text/plain",
    )
) -> str:
    if not payload:
        raise HTTPException(
            status_code=422,
            detail="The body is required"
        )
    return payload

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    payload: str = Depends(validate_payload_from_query),
    selected_model: GigaChatModel = Depends(validate_model),
    no_cache: Optional[int] = Query(default=None, description="Set to 1 to skip cache"),
    _: None = Depends(verify_token),
) -> Any:
    return chat(payload, selected_model, no_cache=(no_cache == 1))

@app.post(
    "/gigachat/chat",
    summary="Send a message to GigaChat",
    description="Accepts a message in body and sends it to GigaChat"
)
async def _(
    payload: str = Depends(validate_payload_from_body),
    selected_model: GigaChatModel = Depends(validate_model),
    no_cache: Optional[int] = Query(default=None, description="Set to 1 to skip cache"),
    _: None = Depends(verify_token),
) -> Any:
    return chat(payload, selected_model, no_cache=(no_cache == 1))
