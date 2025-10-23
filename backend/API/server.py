from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct"  # ✅ correct model id
HF_TOKEN = os.getenv("HF_TOKEN")                 # keep this in .env (server-side only)

client = InferenceClient(model=MODEL, token=HF_TOKEN)

app = FastAPI()

# allow your React dev server to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # adjust for your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskBody(BaseModel):
    query: str

@app.post("/api/ask")
def ask(body: AskBody):
    messages = [
        {"role": "system", "content": "You are a concise product-research assistant."},
        {"role": "user",   "content": body.query}
    ]

    text = []
    for event in client.chat.completions.create(
        model=MODEL, messages=messages, max_tokens=350, temperature=0.2, stream=True
    ):
        delta = event.choices[0].delta.content or ""
        text.append(delta)

    return {"answer": "".join(text)}
