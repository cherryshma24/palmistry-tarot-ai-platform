from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

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
# REQUEST MODEL
# ============================================================

class TarotSelectionRequest(BaseModel):

    spread: str

    card_names: list[str]


# ============================================================
# GET COMPLETE TAROT DECK
# ============================================================

@router.get("/deck")
def get_tarot_deck():
    """
    Return all 78 Tarot cards for the frontend.

    No card is randomly selected here.
    """

    return {
        "success": True,
        "cards": tarot_service.get_deck()
    }

# ============================================================
# TAROT IMAGE
# ============================================================

TAROT_IMAGES_DIR = (
    Path(__file__).resolve().parents[2]
    / "datasets"
    / "tarot"
    / "images"
)


@router.get("/image/{filename}")
async def get_tarot_image(filename: str):

    # Prevent invalid paths
    safe_filename = Path(filename).name

    image_path = TAROT_IMAGES_DIR / safe_filename

    print("========================================")
    print("TAROT IMAGE REQUEST")
    print("Filename:", safe_filename)
    print("Image path:", image_path)
    print("Exists:", image_path.exists())
    print("========================================")

    if not image_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Tarot image not found: {safe_filename}"
        )

    return FileResponse(
        image_path,
        media_type="image/jpeg"
    )

# ============================================================
# SELECTED TAROT READING
# ============================================================

@router.post("/selected")
def selected_tarot_reading(
    request: TarotSelectionRequest
):
    """
    Generate a Tarot reading using the exact cards
    selected by the user.

    Single:
        one selected card

    Three:
        Past → Present → Future
    """

    # --------------------------------------------------------
    # SINGLE CARD
    # --------------------------------------------------------

    if request.spread == "single":

        if len(request.card_names) != 1:

            raise HTTPException(
                status_code=400,
                detail="Please select exactly one Tarot card."
            )

        result = tarot_service.selected_single_card_reading(
            request.card_names[0]
        )

        if not result:

            raise HTTPException(
                status_code=400,
                detail="Selected Tarot card was not found."
            )


    # --------------------------------------------------------
    # THREE CARD
    # --------------------------------------------------------

    elif request.spread == "three":

        if len(request.card_names) != 3:

            raise HTTPException(
                status_code=400,
                detail="Please select exactly three Tarot cards."
            )

        result = tarot_service.selected_three_card_reading(
            request.card_names
        )

        if not result:

            raise HTTPException(
                status_code=400,
                detail="One or more selected Tarot cards were not found."
            )


    # --------------------------------------------------------
    # INVALID SPREAD
    # --------------------------------------------------------

    else:

        raise HTTPException(
            status_code=400,
            detail="Invalid Tarot spread."
        )


    # --------------------------------------------------------
    # STORE EXACT READING
    # --------------------------------------------------------

    state.latest_tarot_reading = result


    return result