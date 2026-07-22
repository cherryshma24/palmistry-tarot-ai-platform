class TarotInterpreter:

    def interpret_card(self, card):
        """
        Convert raw JSON card into readable API response.
        """

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

            "light_meaning": card.get(
                "meanings",
                {}
            ).get("light", []),

            "shadow_meaning": card.get(
                "meanings",
                {}
            ).get("shadow", []),

            "archetype": card.get(
                "Archetype",
                "Not Available"
            ),

            "hebrew_alphabet": card.get(
                "Hebrew Alphabet",
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