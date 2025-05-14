import time
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from sse_starlette.sse import EventSourceResponse
import asyncio
from typing import AsyncGenerator
from schemas.chat import ChatRequest
import logging

from services.openai_service import process_chat_with_tools

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/health")
async def health_check():
    return {"status": "ok healtha"}

async def stream_response(message: str) -> AsyncGenerator[str, None]:
    logger.info(f"Starting stream response for message: {message}")
    try:
        async for chunk in process_chat_with_tools(message):
            if chunk:  # Only yield non-empty chunks
                logger.info(f"Received chunk from process_chat_with_tools: {chunk}")
                yield f"data: {chunk}\n\n"
                await asyncio.sleep(0.25)  # Add a 100ms delay between chunks
    except Exception as e:
        logger.error(f"Error in stream_response: {str(e)}")
        yield f"data: Error: {str(e)}\n\n"

@router.post("/chat")
async def chat(request: ChatRequest):
    """Chat endpoint that streams weather information"""
    logger.info(f"Received chat request: {request.message}")
    return EventSourceResponse(stream_response(request.message)) 

