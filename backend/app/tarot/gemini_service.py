import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiService:
    """
    Handles AI-generated Tarot interpretations using Gemini.
    """

    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def generate_reading(self, card):
        """
        Generate AI interpretation for a single tarot card.
        """

        prompt = f"""
You are an experienced tarot guide.

Card Details

Name:
{card.get("name")}

Arcana:
{card.get("arcana")}

Keywords:
{", ".join(card.get("keywords", []))}

Positive Meanings:
{", ".join(card.get("light_meaning", []))}

Shadow Meanings:
{", ".join(card.get("shadow_meaning", []))}

Generate a natural tarot reading.

Return only plain text.

Include:

1. Overall Meaning
2. Personality Insights
3. Career Guidance
4. Relationship Guidance
5. Self-Reflection Advice

Do not make guaranteed predictions.
Keep the tone encouraging and reflective.
"""

        try:

            response = self.client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            return f"Unable to generate AI reading: {str(e)}"

    def generate_three_card_reading(self, past, present, future):
        """
        Generate one AI interpretation for a Past-Present-Future spread.
        """

        prompt = f"""
You are an experienced Tarot Reader.

Interpret the following Past-Present-Future tarot spread.

----------------------------------------
PAST CARD
----------------------------------------

Name:
{past.get("name")}

Keywords:
{", ".join(past.get("keywords", []))}

Positive Meanings:
{", ".join(past.get("light_meaning", []))}

Shadow Meanings:
{", ".join(past.get("shadow_meaning", []))}

----------------------------------------
PRESENT CARD
----------------------------------------

Name:
{present.get("name")}

Keywords:
{", ".join(present.get("keywords", []))}

Positive Meanings:
{", ".join(present.get("light_meaning", []))}

Shadow Meanings:
{", ".join(present.get("shadow_meaning", []))}

----------------------------------------
FUTURE CARD
----------------------------------------

Name:
{future.get("name")}

Keywords:
{", ".join(future.get("keywords", []))}

Positive Meanings:
{", ".join(future.get("light_meaning", []))}

Shadow Meanings:
{", ".join(future.get("shadow_meaning", []))}

----------------------------------------

Create ONE complete tarot reading.

Include these sections:

1. Past Influence
2. Present Situation
3. Future Direction
4. Career Guidance
5. Relationship Guidance
6. Personal Growth
7. Overall Summary

Do not make guaranteed future predictions.

Use a warm, thoughtful, encouraging tone.

Return only plain text.
"""

        try:

            response = self.client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            return f"Unable to generate AI reading: {str(e)}"