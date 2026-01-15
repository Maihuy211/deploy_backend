from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ChatRequest(BaseModel):
    messages: list

@app.get("/")
def root():
    return {"status": "Backend running"}

@app.post("/api/chat")
async def chat(req: ChatRequest):
    if not OPENAI_API_KEY:
        raise HTTPException(500, "Missing OPENAI_API_KEY")

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": req.messages,
        "temperature": 0.7,
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
        )

    return res.json()
