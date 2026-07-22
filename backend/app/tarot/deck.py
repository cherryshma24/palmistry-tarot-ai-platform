import random

from app.tarot.cards import TAROT_DATA


def shuffle_deck():
    deck = TAROT_DATA.copy()
    random.shuffle(deck)
    return deck


def draw_cards(number=1):
    deck = shuffle_deck()
    return deck[:number]