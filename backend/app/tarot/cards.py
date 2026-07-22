import json
import os

DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "datasets",
    "tarot",
    "cards.json"
)

with open(DATA_PATH, "r", encoding="utf-8") as file:
    TAROT_DATA = json.load(file)["cards"]