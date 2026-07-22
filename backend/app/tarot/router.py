from fastapi import APIRouter

from app.tarot.service import TarotService

router = APIRouter(
    prefix="/tarot",
    tags=["Tarot Reading"]
)

# Create one service object
tarot_service = TarotService()


@router.get("/single")
def single_card():
    """
    Draw a random tarot card.
    """
    return tarot_service.single_card_reading()


@router.get("/three")
def three_card():
    """
    Past • Present • Future spread.
    """
    return tarot_service.three_card_reading()