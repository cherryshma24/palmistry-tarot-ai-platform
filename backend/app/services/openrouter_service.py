import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# LOAD .ENV
# ============================================================

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_path)

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise Exception("OPENROUTER_API_KEY not found in .env")


# ============================================================
# OPENROUTER CLIENT
# ============================================================

client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1",
)


# ============================================================
# MODEL
# ============================================================
#
# OpenRouter's free router automatically selects an available
# free model.
#
# This is the same model configuration that successfully
# worked in our Colab test.
#

MODEL = "openrouter/free"


# ============================================================
# ASK AI
# ============================================================

def ask_ai(prompt: str):
    """
    Send a prompt to OpenRouter and return the AI response.

    Used by:
        - Palm Reading
        - Personality Intelligence
        - Tarot Intelligence
    """

    system_prompt = (
        "You are an expert Palmistry and Tarot AI. "
        "Analyze only the information supplied in the prompt. "
        "Do not invent measurements, detections, or observations. "
        "Provide positive, detailed and natural interpretations. "
        "Palmistry and tarot are for entertainment and "
        "self-reflection only. "
        "Never claim supernatural or scientific certainty. "
        "Return clean JSON whenever JSON is requested."
    )

    try:

        print(f"\nOpenRouter Model: {MODEL}")

        response = client.chat.completions.create(
            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],

            temperature=0.4,
            max_tokens=1800,
        )

        result = response.choices[0].message.content

        if not result:
            raise Exception("OpenRouter returned an empty response.")

        print(f"OpenRouter AI response received successfully.")

        return result.strip()

    except Exception as e:

        print("OpenRouter request failed.")
        print(f"Error: {e}")

        raise Exception(
            f"OpenRouter AI request failed: {e}"
        )