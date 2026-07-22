import json
import os
import random


class TarotService:

    def __init__(self):

        path = os.path.join(
            "datasets",
            "tarot",
            "cards.json"
        )

        with open(path, "r", encoding="utf-8") as file:
            self.cards = json.load(file)


    def draw_cards(self):

        selected = random.sample(
            self.cards,
            3
        )

        positions = [
            "Past",
            "Present",
            "Future"
        ]

        result=[]

        for card, position in zip(selected, positions):

            result.append({

                "name": card["name"],

                "position": position,

                "meaning": card["meaning"]

            })


        return result