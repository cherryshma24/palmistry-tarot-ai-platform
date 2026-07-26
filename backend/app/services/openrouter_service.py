import os
import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# -----------------------------
# Load .env
# -----------------------------
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_path)

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise Exception("OPENROUTER_API_KEY not found in .env")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "google/gemma-4-31b-it:free"


def ask_ai(prompt: str):
    """
    Send a prompt to OpenRouter and return the response text.
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert Palmistry and Tarot AI. "
"You analyze palm features and tarot cards. "
"Provide positive, detailed, natural interpretations. "
"Never claim supernatural certainty. "
"Return clean JSON when requested."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.7,
        max_tokens=1200,
    )

    return response.choices[0].message.content.strip()