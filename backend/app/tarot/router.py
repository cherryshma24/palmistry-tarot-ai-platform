from fastapi import APIRouter

from app.tarot.service import TarotService
from app.palm import state


router = APIRouter(
    prefix="/tarot",
    tags=["Tarot Reading"]
)


# ============================================================
# CREATE TAROT SERVICE
# ============================================================

tarot_service = TarotService()


# ============================================================
# SINGLE CARD
# ============================================================

@router.get("/single")
def single_card():
    """
    Draw a random Tarot card.

    The exact reading returned to the user is stored
    so the Report module can use the same card later.
    """

    result = tarot_service.single_card_reading()

    # Store the exact Tarot result
    state.latest_tarot_reading = result

    return result


# ============================================================
# THREE CARD
# ============================================================

@router.get("/three")
def three_card():
    """
    Generate a Past • Present • Future Tarot spread.

    The exact three-card reading is stored so the
    Report module can use the same cards later.
    """

    result = tarot_service.three_card_reading()

    # Store the exact Tarot result
    state.latest_tarot_reading = result

    return result