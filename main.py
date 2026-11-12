from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from groq import Groq
import requests, os, json, random

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

client = Groq(api_key=GROQ_API_KEY)

app = FastAPI(title="Adhu Bhai")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def adhu_ai(city, weather):
    prompt = f"""
You are Adhu Bhai — a funny, friendly Mumbai-style AI assistant.

Reply ONLY in valid JSON. No extra text.

City: {city}

Format:
{{
  "speech": "Fun Mumbai slang line about the city",
  "emotion": "excited | confident | chill",
  "eyes": "normal | wide | narrow"
}}

Rules:
- Max 1–2 short sentences
- Natural variation every time
"""

    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )

    raw = r.choices[0].message.content.strip()
    start = raw.find("{")
    end = raw.rfind("}") + 1
    return json.loads(raw[start:end])

@app.get("/agent")
def agent(city: str):
    w = requests.get(
        "http://api.weatherapi.com/v1/current.json",
        params={"key": WEATHER_API_KEY, "q": city}
    ).json()

    if "error" in w:
        return {"error": "City nahi mila bhidu"}

    weather = {
        "temp": w["current"]["temp_c"],
        "humidity": w["current"]["humidity"],
        "condition": w["current"]["condition"]["text"]
    }

    try:
        ai = adhu_ai(city, weather)
    except Exception as e:
        print("LLM ERROR:", e)
        ai = {
            "speech": random.choice([
                f"{city} ka scene full jhakaas hai bhidu 😎",
                f"Bole toh {city} mast vibe de raha hai bhidu 🔥",
                f"{city} aaj proper mood mein hai bhidu 😏"
            ]),
            "emotion": random.choice(["confident", "chill"]),
            "eyes": random.choice(["normal", "wide"])
        }

    return {
        "agent": ai,
        "weather": weather
    }