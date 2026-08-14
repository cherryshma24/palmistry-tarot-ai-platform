import json
import os
import random

from app.tarot.report import TarotReport
from app.services.openrouter_service import ask_ai


class TarotService:

    def __init__(self):
        """
        Load all tarot cards from cards.json.
        """

        dataset = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "datasets",
            "tarot",
            "cards.json"
        )

        dataset = os.path.abspath(dataset)

        with open(dataset, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.cards = data["cards"]

    # =========================================================
    # GET CARD
    # =========================================================

    def get_card(self, card_name: str):
        """
        Return a card by its name.
        """

        for card in self.cards:

            if card.get("name", "").lower() == card_name.lower():
                return card

        return None

    # =========================================================
    # DRAW RANDOM CARD
    # =========================================================

    def draw_random_card(self):
        """
        Draw one random tarot card.
        """

        return random.choice(self.cards)

    # =========================================================
    # DRAW MULTIPLE CARDS
    # =========================================================

    def draw_multiple_cards(self, count: int):
        """
        Draw multiple unique tarot cards.
        """

        count = min(count, len(self.cards))

        return random.sample(self.cards, count)

    # =========================================================
    # INTERPRET CARD
    # =========================================================

    def interpret_card(self, card):
        """
        Convert raw JSON card into readable API response.
        """

        meanings = card.get("meanings", {})

        return {

            "name": card.get("name"),

            "number": card.get("number"),

            "arcana": card.get("arcana"),

            "suit": card.get("suit"),

            "image": card.get("img"),

            "keywords": card.get("keywords", []),

            "fortune_telling": card.get(
                "fortune_telling",
                []
            ),

            "light_meaning": meanings.get(
                "light",
                []
            ),

            "shadow_meaning": meanings.get(
                "shadow",
                []
            ),

            "archetype": card.get(
                "Archetype",
                "Not Available"
            ),

            "numerology": card.get(
                "Numerology",
                "Not Available"
            ),

            "element": card.get(
                "Elemental",
                "Not Available"
            ),

            "mythical_spiritual": card.get(
                "Mythical/Spiritual",
                "Not Available"
            ),

            "questions_to_ask": card.get(
                "Questions to Ask",
                []
            )
        }

    # =========================================================
    # AI READING
    # =========================================================

    def generate_ai_reading(self, prompt):

        try:

            response = ask_ai(prompt)

            if response:
                return response.strip()

        except Exception as e:

            print(
                "OpenRouter Tarot Error:",
                e
            )

        return (
            "This tarot reading represents guidance, "
            "self-reflection, personal growth, and "
            "new possibilities."
        )

    # =========================================================
    # GENERATE READING FOR EXISTING CARD
    # =========================================================

    def generate_reading_for_card(self, card):
        """
        Generate a Tarot reading for an already selected card.

        IMPORTANT:
        This method does NOT draw a new card.

        It is used when the Report module needs to generate
        a report from the exact Tarot card the user already
        received.
        """

        if not card:
            return None

        reading = self.interpret_card(card)

        prompt = f"""
You are an expert Tarot reader.

Analyze this tarot card and provide a meaningful spiritual interpretation.

Card Information:

{json.dumps(reading, indent=2)}

Explain:

- Personality insights
- Opportunities
- Challenges
- Emotional guidance
- Career and life direction

Return a positive and detailed reading.
Do not mention you are an AI.
"""

        ai_reading = self.generate_ai_reading(
            prompt
        )

        return {

            "success": True,

            "spread": "Single Card",

            "card": reading,

            "report": TarotReport.generate(
                reading
            ),

            "ai_reading": ai_reading
        }

    # =========================================================
    # SINGLE CARD READING
    # =========================================================

    def single_card_reading(self):
        """
        Generate a Single Card Reading.

        A random card is drawn ONLY here.

        After the card is drawn, the same card is passed
        to generate_reading_for_card().
        """

        card = self.draw_random_card()

        return self.generate_reading_for_card(
            card
        )

    # =========================================================
    # THREE CARD READING
    # =========================================================

    def three_card_reading(self):
        """
        Past • Present • Future Reading.
        """

        cards = self.draw_multiple_cards(3)

        past = self.interpret_card(
            cards[0]
        )

        present = self.interpret_card(
            cards[1]
        )

        future = self.interpret_card(
            cards[2]
        )

        prompt = f"""
You are an expert Tarot reader.

Generate a Past, Present, Future tarot interpretation.

Past Card:
{json.dumps(past, indent=2)}

Present Card:
{json.dumps(present, indent=2)}

Future Card:
{json.dumps(future, indent=2)}

Explain:

- Past influences
- Current situation
- Future possibilities
- Personal growth guidance
- Overall life message

Return a positive and detailed reading.
Do not mention you are an AI.
"""

        ai_reading = self.generate_ai_reading(
            prompt
        )

        return {

            "success": True,

            "spread":
                "Past • Present • Future",

            "cards": {

                "past": past,

                "present": present,

                "future": future
            },

            "reports": {

                "past":
                    TarotReport.generate(
                        past
                    ),

                "present":
                    TarotReport.generate(
                        present
                    ),

                "future":
                    TarotReport.generate(
                        future
                    )
            },

            "ai_reading": ai_reading
        }