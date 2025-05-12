🧾 Product Requirements Document (PRD)
🧠 Project Title: Local Weather Chat Agent with FastAPI
📌 Objective
Build a chat agent where a user can ask weather-related queries (e.g., “What’s the weather in Paris?”) in natural language. The chatbot will process the query, recognize the city, and respond with the weather information using a tool call to a backend Python function that returns hardcoded weather data.

All services should run locally using FastAPI and be invokable via Postman. Responses must support server-sent events (SSE) to enable streaming.

🎯 Core Features
1. 🧠 Chat Agent
Accepts natural language input like:

“What's the weather in Delhi?”

“Is it raining in Tokyo?”

Parses city names from input.

Uses a tool-calling mechanism to invoke a Python function that returns weather.

2. 🛠️ Tool Call Function (Hardcoded Weather Provider)
Function: get_weather(city_name: str) -> str

Returns weather for a limited set of cities:

python
Copy
Edit
{
  "Delhi": "Sunny, 35°C",
  "London": "Cloudy, 20°C",
  "New York": "Rainy, 15°C",
  "Tokyo": "Clear, 25°C",
  "Paris": "Windy, 22°C"
}
If city is unknown, respond: “Sorry, I don’t have data for that city.”

3. 🚀 API Endpoints (FastAPI)
a. GET /health
Purpose: Health check endpoint.

Response: {"status": "ok"}

b. POST /chat (SSE)
Type: Server-Sent Events (SSE).

Input (JSON):

json
Copy
Edit
{
  "message": "What's the weather in London?"
}
Process:

Parse input.

Extract city.

Call get_weather(city) function.

Stream the reply using SSE (simulate typing delay if needed).

Output (streamed text):

csharp
Copy
Edit
The weather in London is Cloudy, 20°C.
🖥️ Runtime Environment
Backend
Language: Python 3.10+

Framework: FastAPI

Streaming: fastapi.responses.EventSourceResponse

Execution
Local development using univorn (uvicorn).

Install requirements with pip install -r requirements.txt

Run server: uvicorn main:app --reload

Testable via Postman (set "Accept" header to text/event-stream for streaming).

🧪 Testing
Use Postman to hit /health and /chat endpoints.

/chat should return streamed weather data.

Validate correct response for valid cities and error message for unknown cities.