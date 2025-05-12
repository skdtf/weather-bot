# Weather Chat Bot

A FastAPI-based chatbot that provides weather information for various cities using OpenAI's GPT model with tool calling and Server-Sent Events (SSE).

## Features

- OpenAI GPT integration with tool calling
- Natural language processing for weather queries
- Server-Sent Events (SSE) for streaming responses
- Hardcoded weather data for major cities
- Health check endpoint
- CORS enabled for cross-origin requests

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your OpenAI API key:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

## API Endpoints

### Health Check
- **GET** `/api/health`
- Response: `{"status": "ok"}`

### Chat
- **POST** `/api/chat`
- Request Body:
```json
{
    "message": "What's the weather in London?"
}
```
- Response: Server-Sent Events stream with weather information

## Testing with Postman

1. For the chat endpoint:
   - Set the request type to POST
   - URL: `http://localhost:8000/api/chat`
   - Headers: 
     - `Content-Type: application/json`
     - `Accept: text/event-stream`
   - Body (raw JSON):
   ```json
   {
       "message": "What's the weather in London?"
   }
   ```

2. For the health check:
   - Set the request type to GET
   - URL: `http://localhost:8000/api/health`

## Available Cities

The bot currently supports weather information for:
- Delhi
- London
- New York
- Tokyo
- Paris
- And many more cities (see weather_tool.py for complete list)

## How it Works

1. The user sends a natural language query about weather
2. The OpenAI model processes the query and decides to use the weather tool
3. The tool call is made to our `get_weather` function
4. The weather information is returned to the model
5. The model formats a natural response
6. The response is streamed back to the user with a typing effect 