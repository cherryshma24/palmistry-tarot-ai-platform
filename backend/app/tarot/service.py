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
    # GET COMPLETE TAROT DECK
    # =========================================================

    def get_deck(self):
        """
        Return the tarot deck for the frontend.

        Only safe information required by the card-selection
        screen is returned.
        """

        deck = []

        for card in self.cards:

            deck.append({

                "name": card.get("name"),

                "image": card.get("img"),

                "number": card.get("number"),

                "arcana": card.get("arcana"),

                "suit": card.get("suit")

            })

        return deck

    # =========================================================
    # DRAW RANDOM CARD
    # =========================================================

    def draw_random_card(self):
        """
        Draw one random tarot card.

        Kept for backward compatibility.
        """

        return random.choice(self.cards)

    # =========================================================
    # DRAW MULTIPLE CARDS
    # =========================================================

    def draw_multiple_cards(self, count: int):
        """
        Draw multiple unique tarot cards.

        Kept for backward compatibility.
        """

        count = min(count, len(self.cards))

        return random.sample(self.cards, count)

    # =========================================================
    # GET USER SELECTED CARDS
    # =========================================================

    def get_selected_cards(
        self,
        card_names,
        spread
    ):
        """
        Get the exact cards selected by the user.

        IMPORTANT:
        This method DOES NOT randomly select cards.
        """

        if not isinstance(card_names, list):
            return None

        if spread == "single":

            if len(card_names) != 1:
                return None

        elif spread == "three":

            if len(card_names) != 3:
                return None

            # Prevent selecting the same card more than once

            if len(set(card_names)) != 3:
                return None

        else:
            return None

        selected_cards = []

        for card_name in card_names:

            card = self.get_card(
                card_name
            )

            if not card:
                return None

            selected_cards.append(card)

        return selected_cards

    # =========================================================
    # INTERPRET CARD
    # =========================================================

    def interpret_card(self, card):
        """
        Convert raw JSON card into readable API response.
        """

        meanings = card.get(
            "meanings",
            {}
        )

        return {

            "name": card.get("name"),

            "number": card.get("number"),

            "arcana": card.get("arcana"),

            "suit": card.get("suit"),

            "image": card.get("img"),

            "keywords": card.get(
                "keywords",
                []
            ),

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

            response = ask_ai(
                prompt
            )

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
        Generate a reading for an already selected card.

        This does NOT draw another card.
        """

        if not card:
            return None

        reading = self.interpret_card(
            card
        )

        prompt = f"""
You are an expert Tarot reader.

Analyze this tarot card and provide a meaningful,
positive and insightful interpretation.

Card Information:

{json.dumps(reading, indent=2)}

Explain:

- Personality insights
- Opportunities
- Challenges
- Emotional guidance
- Career and life direction
- Personal growth

IMPORTANT:

- Do not claim supernatural certainty.
- Do not make guaranteed future predictions.
- Tarot is for entertainment and self-reflection.
- Do not mention that you are an AI.

Return a natural and detailed interpretation.
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
    # GENERATE READING FROM USER SELECTED SINGLE CARD
    # =========================================================

    def selected_single_card_reading(
        self,
        card_name
    ):
        """
        Generate reading from the exact card selected
        by the user.
        """

        selected = self.get_selected_cards(
            [card_name],
            "single"
        )

        if not selected:
            return None

        return self.generate_reading_for_card(
            selected[0]
        )

    # =========================================================
    # GENERATE THREE CARD READING
    # =========================================================

    def selected_three_card_reading(
        self,
        card_names
    ):
        """
        Generate Past / Present / Future reading from
        the exact three cards selected by the user.
        """

        selected = self.get_selected_cards(
            card_names,
            "three"
        )

        if not selected:
            return None

        past = self.interpret_card(
            selected[0]
        )

        present = self.interpret_card(
            selected[1]
        )

        future = self.interpret_card(
            selected[2]
        )

        prompt = f"""
You are an expert Tarot reader.

Generate a Past, Present, Future tarot interpretation
using ONLY the three cards supplied below.

PAST CARD:

{json.dumps(past, indent=2)}

PRESENT CARD:

{json.dumps(present, indent=2)}

FUTURE CARD:

{json.dumps(future, indent=2)}

Explain:

- Past influences
- Current situation
- Future possibilities
- Personal growth guidance
- Overall life message

IMPORTANT:

- Do not claim supernatural certainty.
- Do not make guaranteed future predictions.
- Tarot is for entertainment and self-reflection.
- Do not invent cards.
- Do not mention that you are an AI.

Return a positive, natural and detailed interpretation.
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

    # =========================================================
    # OLD RANDOM SINGLE READING
    # =========================================================

    def single_card_reading(self):

        card = self.draw_random_card()

        return self.generate_reading_for_card(
            card
        )

    # =========================================================
    # OLD RANDOM THREE CARD READING
    # =========================================================

    def three_card_reading(self):

        cards = self.draw_multiple_cards(
            3
        )

        return self.selected_three_card_reading(
            [
                cards[0]["name"],
                cards[1]["name"],
                cards[2]["name"]
            ]
        )