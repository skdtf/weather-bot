from openai import AsyncOpenAI
from typing import Dict, Any, AsyncGenerator
from core.config import get_settings
from services.weather_tool import get_weather
import logging


settings = get_settings()
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_weather_tool_schema() -> Dict[str, Any]:
    """Define the schema for the weather tool"""
    return {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a specific city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city to get weather for"
                    }
                },
                "required": ["city"]
            }
        }
    }

    
async def process_chat_with_tools(message: str) -> AsyncGenerator[str, None]:
    logger.info(f"Processing message: {message}")
    
    messages = [
        {
            "role": "system",
            "content": "You are a helpful weather assistant. Use the get_weather tool to provide weather information. If the user doesn't specify a city, ask for clarification instead of assuming"
        },
        {"role": "user", "content": message}
    ]

    tools = [get_weather_tool_schema()]
    logger.info("Making initial API call to OpenAI")

    response = await client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        stream=True
    )

    buffered_chunks = []
    tool_call = None
    tool_arguments = ""
    tool_call_id = None
    tool_name = None

    async for chunk in response:
        if not chunk.choices:
            continue
            
        delta = chunk.choices[0].delta
        logger.info(f"Received chunk: {delta}")

        if delta.tool_calls:
            current_tool_call = delta.tool_calls[0]
            if not tool_call_id:
                tool_call_id = current_tool_call.id
                tool_name = current_tool_call.function.name
            if hasattr(current_tool_call.function, 'arguments'):
                tool_arguments += current_tool_call.function.arguments or ""
                logger.info(f"Accumulated tool arguments: {tool_arguments}")
            continue

        if delta.content:
            buffered_chunks.append(delta.content)
            logger.info(f"Buffered content: {delta.content}")

    logger.info(f"Final tool call - ID: {tool_call_id}, Name: {tool_name}, Arguments: {tool_arguments}")

    if tool_call_id and tool_name == "get_weather" and tool_arguments:
        try:
            import json
            args = json.loads(tool_arguments)
            city = args.get("city")
            logger.info(f"Extracted city: {city}")
            
            weather_info = get_weather(city)
            logger.info(f"Weather info: {weather_info}")

            messages.append({
                "role": "assistant",
                "content": None,
                "tool_calls": [{
                    "id": tool_call_id,
                    "type": "function",
                    "function": {
                        "name": "get_weather",
                        "arguments": tool_arguments
                    }
                }]
            })
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": weather_info
            })

            logger.info(f"Messages: {messages}")
            logger.info("Making final API call to OpenAI")
            final_response = await client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=messages,
                stream=True
            )

            async for chunk in final_response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    logger.info(f"Yielding content: {content}")
                    yield content
        except Exception as e:
            logger.error(f"Error processing tool call: {str(e)}")
            yield f"Error processing request: {str(e)}"
    else:
        logger.info("No tool call, yielding buffered chunks")
        for text in buffered_chunks:
            logger.info(f"Yielding buffered text: {text}")
            yield text

