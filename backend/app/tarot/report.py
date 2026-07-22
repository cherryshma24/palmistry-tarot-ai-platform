class TarotReport:
    """
    Generates a human-readable Tarot Reading Report.
    """

    @staticmethod
    def generate(card: dict):

        report = f"""
==========================================
          TAROT READING REPORT
==========================================

🔮 Card Drawn
-------------
Name       : {card.get("name", "Not Available")}
Arcana     : {card.get("arcana", "Not Available")}
Suit       : {card.get("suit", "Not Available")}
Number     : {card.get("number", "Not Available")}

⭐ Keywords
-----------
{", ".join(card.get("keywords", [])) if card.get("keywords") else "Not Available"}

✨ Fortune Telling
-----------------
"""

        fortunes = card.get("fortune_telling", [])

        if fortunes:
            for item in fortunes:
                report += f"• {item}\n"
        else:
            report += "Not Available\n"

        report += "\n🌞 Positive Meanings\n-------------------\n"

        positives = card.get("light_meaning", [])

        if positives:
            for item in positives:
                report += f"• {item}\n"
        else:
            report += "Not Available\n"

        report += "\n🌑 Shadow Meanings\n-----------------\n"

        shadows = card.get("shadow_meaning", [])

        if shadows:
            for item in shadows:
                report += f"• {item}\n"
        else:
            report += "Not Available\n"

        report += f"""

🧠 Archetype
------------
{card.get("archetype", "Not Available")}

🔢 Numerology
-------------
{card.get("numerology", "Not Available")}

🌍 Element
----------
{card.get("element", "Not Available")}

✨ Mythical / Spiritual
-----------------------
{card.get("mythical_spiritual", "Not Available")}

❓ Reflection Questions
-----------------------
"""

        questions = card.get("questions_to_ask", [])

        if questions:
            for question in questions:
                report += f"• {question}\n"
        else:
            report += "No reflection questions available.\n"

        report += """

==========================================
Overall Guidance
==========================================

Every tarot card represents guidance rather than certainty.
Use this reading as a source of reflection, self-awareness,
and thoughtful decision-making.

Trust your intuition, stay open to new possibilities,
and use today's insights to guide your actions positively.

==========================================
"""

        return report