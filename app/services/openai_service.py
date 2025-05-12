from openai import OpenAI
from typing import Dict, Any
from core.config import get_settings
from services.weather_tool import get_weather

settings = get_settings()
client = OpenAI(api_key=settings.OPENAI_API_KEY)

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

def process_chat_with_tools(message: str) -> str:
    messages = [
        {"role": "system", "content": "You are a helpful weather assistant. Use the get_weather tool to provide weather information. If the user doesn’t specify a city, ask for clarification instead of assuming"},
        {"role": "user", "content": message}
    ]
    
    tools = [get_weather_tool_schema()]
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    response_message = response.choices[0].message

    print(f'response_message: {response_message}')
    
    # Check if the model wants to call a tool
    if response_message.tool_calls:
        tool_call = response_message.tool_calls[0]
        if tool_call.function.name == "get_weather":
            # Parse the arguments
            import json
            args = json.loads(tool_call.function.arguments)
            city = args.get("city")
            
            # Get weather using our function
            weather_info = get_weather(city)
            
            # Add the tool response to messages
            messages.append(response_message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": weather_info
            })
            
            # Get final response
            final_response = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=messages
            )
            if not final_response.choices[0].message.content.strip():
                return weather_info
            return final_response.choices[0].message.content
    
    return response_message.content or "Sorry, I couldn't get the weather."
