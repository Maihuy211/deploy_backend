import os
import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


@app.get("/")
def home():
    return {"status": "ok"}


@app.post("/api/chat")
async def chat(req: Request):
    body = await req.json()
    message = body.get("message")

    if not message:
        return {"error": "Message is required"}

    if not GEMINI_API_KEY:
        return {"error": "Missing GEMINI_API_KEY"}

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [{"text": message}]
            }
        ]
    }

    try:
        res = requests.post(url, json=payload, timeout=60)
        data = res.json()

        if "candidates" not in data:
            return {"error": str(data)}

        reply = data["candidates"][0]["content"]["parts"][0]["text"]

        return {"reply": reply}

    except Exception as e:
        return {"error": str(e)}
