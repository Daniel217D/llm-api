from typing import Any
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from gigachat import GigaChat

from app.token_manager import get_or_refresh_token

app = FastAPI()

@app.get("/")
async def hello_world() -> Any:
    with GigaChat(access_token=get_or_refresh_token(), verify_ssl_certs=False, model="GigaChat") as giga:
        response = giga.chat("Привет, как дела?")
        print(response)
        return response.choices[0].message.content
 