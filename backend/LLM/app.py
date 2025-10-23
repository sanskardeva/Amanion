# app.py
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

MODEL = "meta-llama/Llama-3.1-8B-Instruct"  
HF_TOKEN = os.getenv("HF_TOKEN")    # only required for gated models like Llama

client = InferenceClient(model=MODEL, token=HF_TOKEN)

messages = [
    {"role": "system", "content": "You are a concise product-research assistant."},
    {"role": "user", "content": "is mac better than windows?"}
]

# Streaming chat completion
for event in client.chat.completions.create(
    model=MODEL,
    messages=messages,
    max_tokens=300,
    temperature=0.2,
    stream=True,
):
    delta = event.choices[0].delta.content or ""
    print(delta, end="", flush=True)

print()