import json

from app.services.gemini_service import generate_text


class AIManager:

    def generate_reading(self, card):

        prompt = f"""
You are an expert Tarot reader.

Card:
{json.dumps(card, indent=2)}

Generate a warm, positive and insightful tarot reading.

Include:
- Overall interpretation
- Love
- Career
- Finance
- Health
- Spiritual guidance

Write naturally in plain English.
"""

        try:

            response = generate_text(prompt)

            if response:
                return response

        except Exception as e:

            print("Gemini Error:", e)

        # -------- Fallback --------

        keywords = ", ".join(card.get("keywords", []))
        fortunes = ", ".join(card.get("fortune_telling", []))

        return (
            f"This reading is based on '{card.get('name')}'. "
            f"The card highlights themes such as {keywords}. "
            f"{fortunes}. "
            "It encourages personal growth, thoughtful decisions, "
            "balanced relationships and confidence in future opportunities."
        )

    def generate_three_card_reading(self, past, present, future):

        prompt = f"""
You are an expert Tarot reader.

Past:
{json.dumps(past, indent=2)}

Present:
{json.dumps(present, indent=2)}

Future:
{json.dumps(future, indent=2)}

Generate one combined reading.

Include:
- Overall meaning
- Love
- Career
- Finance
- Health
- Spiritual guidance

Write naturally in plain English.
"""

        try:

            response = generate_text(prompt)

            if response:
                return response

        except Exception as e:

            print("Gemini Error:", e)

        # -------- Fallback --------

        return (
            f"Past: {past['name']} indicates lessons learned. "
            f"Present: {present['name']} represents your current path. "
            f"Future: {future['name']} suggests upcoming opportunities. "
            "Together these cards encourage confidence, patience and "
            "steady personal growth."
        )