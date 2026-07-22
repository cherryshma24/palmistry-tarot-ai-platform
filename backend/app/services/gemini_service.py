import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_palm_reading(profile, palm_features):

    print("🔥 GEMINI FUNCTION CALLED")

    prompt = f"""
You are an expert Palmistry AI.

User Profile:
{profile}

Palm Features:
{palm_features}

Generate a positive and natural palm reading.

Return ONLY valid JSON.

{{
    "life_line":"",
    "heart_line":"",
    "head_line":"",
    "fate_line":"",
    "love_prediction":"",
    "career_prediction":"",
    "finance_prediction":"",
    "health_prediction":"",
    "overall_summary":"",
    "fortune_score":90
}}
"""

    try:
        response = client.models.generate_content(
            model="models/gemini-3.5-flash",
            contents=prompt
        )

        print("===== GEMINI RESPONSE =====")
        print(response.text)

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "").strip()

        return json.loads(text)

    except Exception as e:
        print("Gemini Error:", e)

        return {
            "life_line": "Unable to generate.",
            "heart_line": "Unable to generate.",
            "head_line": "Unable to generate.",
            "fate_line": "Unable to generate.",
            "love_prediction": "Unavailable",
            "career_prediction": "Unavailable",
            "finance_prediction": "Unavailable",
            "health_prediction": "Unavailable",
            "overall_summary": str(e),
            "fortune_score": 0
        }