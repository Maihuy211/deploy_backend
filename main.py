import os
import requests
from fastapi import FastAPI, Request, HTTPException
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
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Missing GEMINI_API_KEY")

    body = await req.json()
    message = body.get("message")

    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": message}
                ]
            }
        ]
    }

    try:
        res = requests.post(url, json=payload, timeout=30)
        data = res.json()

        if "candidates" not in data:
            return {"error": data}

        reply = data["candidates"][0]["content"]["parts"][0]["text"]
        return {"reply": reply}

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail="Server error")
