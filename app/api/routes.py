import time
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from sse_starlette.sse import EventSourceResponse
import asyncio
from typing import AsyncGenerator
from schemas.chat import ChatRequest

from services.openai_service import process_chat_with_tools

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok mom2"}

async def stream_response(message: str) -> AsyncGenerator[str, None]:
    response = process_chat_with_tools(message)
    for word in response.split():
        yield f"data: {word}\n\n"
        await asyncio.sleep(0.5)

@router.post("/chat")
async def chat(request: ChatRequest):
    """Chat endpoint that streams weather information"""
    return EventSourceResponse(stream_response(request.message)) 

