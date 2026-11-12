# Adhu Bhai

A small weather app where a cartoon pair of eyes tells you about your city in Mumbai slang.

You type a city name, the backend pulls current weather from WeatherAPI and asks an LLM (Llama 4 Scout on Groq) for a one-line comment in Mumbai street style. The reply also picks an emotion and an eye expression, and the page animates the eyes to match. Temperature, humidity and conditions are shown under the speech line.

If the LLM call fails, the backend falls back to a few canned lines. When the page sits idle, the eyes blink, smirk or look sideways and drop random idle lines.

## How it works

- `main.py` is a FastAPI app with one endpoint, `GET /agent?city=<name>`.
- It returns `{ "agent": { "speech", "emotion", "eyes" }, "weather": { "temp", "humidity", "condition" } }`, or `{ "error": ... }` if the city is not found.
- `index.html` is a single static page (plain HTML/CSS/JS) that calls the backend at `http://127.0.0.1:8000`.

## Stack

- Python, FastAPI, Uvicorn
- Groq Python SDK (`meta-llama/llama-4-scout-17b-16e-instruct`)
- WeatherAPI.com current weather
- Plain HTML/CSS/JS frontend

## Setup

You need a WeatherAPI.com key and a Groq API key. Put them in a `.env` file next to `main.py`:

```
WEATHER_API_KEY=
GROQ_API_KEY=
```

Install and run the backend:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn python-dotenv groq requests
uvicorn main:app --reload --port 8000
```

Then open `index.html` in a browser (directly, or with any static server such as VS Code Live Server), type a city and press the button.

## Notes

- CORS is open to all origins, which is fine for local use only.
- The backend URL is hard-coded in `index.html`; change it there if you run the API elsewhere.
