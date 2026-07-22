import json
import os
import random

from app.tarot.report import TarotReport
from app.tarot.gemini_service import GeminiService


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

        # Initialize Gemini AI
        self.gemini = GeminiService()

    def get_card(self, card_name: str):
        """
        Return a card by its name.
        """

        for card in self.cards:

            if card.get("name", "").lower() == card_name.lower():
                return card

        return None

    def draw_random_card(self):
        """
        Draw one random tarot card.
        """

        return random.choice(self.cards)

    def draw_multiple_cards(self, count: int):
        """
        Draw multiple unique tarot cards.
        """

        count = min(count, len(self.cards))
        return random.sample(self.cards, count)

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

            "fortune_telling": card.get("fortune_telling", []),

            "light_meaning": meanings.get("light", []),

            "shadow_meaning": meanings.get("shadow", []),

            "archetype": card.get("Archetype", "Not Available"),

            "numerology": card.get("Numerology", "Not Available"),

            "element": card.get("Elemental", "Not Available"),

            "mythical_spiritual": card.get(
                "Mythical/Spiritual",
                "Not Available"
            ),

            "questions_to_ask": card.get(
                "Questions to Ask",
                []
            )
        }

    def single_card_reading(self):
        """
        Generate a Single Card Reading.
        """

        card = self.draw_random_card()

        reading = self.interpret_card(card)

        # Generate AI Reading
        ai_reading = self.gemini.generate_reading(reading)

        return {

            "success": True,

            "spread": "Single Card",

            "card": reading,

            # Traditional Report
            "report": TarotReport.generate(reading),

            # Gemini AI Reading
            "ai_reading": ai_reading
        }

    def three_card_reading(self):
        """
        Past • Present • Future Reading.
        """

        cards = self.draw_multiple_cards(3)

        past = self.interpret_card(cards[0])
        present = self.interpret_card(cards[1])
        future = self.interpret_card(cards[2])

        # Generate one AI reading for the complete spread
        ai_reading = self.gemini.generate_three_card_reading(
            past,
            present,
            future
        )

        return {
            "success": True,

            "spread": "Past • Present • Future",

            "cards": {
                "past": past,
                "present": present,
                "future": future
            },

            "reports": {
                "past": TarotReport.generate(past),
                "present": TarotReport.generate(present),
                "future": TarotReport.generate(future)
            },

            "ai_reading": ai_reading
        }