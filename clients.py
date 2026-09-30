import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from groq import Groq

# Load .env from this file's folder
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path, override=True)

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY not found in .env")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")

# Cohere via OpenAI-compatible endpoint
cohere_client = OpenAI(
    api_key=COHERE_API_KEY,
    base_url="https://api.cohere.ai/compatibility/v1",
)

# Groq native client
groq_client = Groq(api_key=GROQ_API_KEY)


def ask_cohere(messages):
    """Send messages to Cohere and return the text reply."""
    response = cohere_client.chat.completions.create(
        model="command-a-03-2025",
        messages=messages,
    )
    return response.choices[0].message.content.strip()


def ask_groq(messages):
    """Send messages to Groq and return the text reply."""
    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
    )
    return response.choices[0].message.content.strip()