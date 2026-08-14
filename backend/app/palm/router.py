from fastapi import APIRouter, UploadFile, File

from app.palm.service import PalmAnalysisService
from app.palm import state


router = APIRouter(
    prefix="/palm",
    tags=["Palm Analysis"]
)


@router.post("/analyze")
async def analyze_palm(
    file: UploadFile = File(...)
):
    """
    Analyze uploaded palm image and store the
    latest result for report generation.
    """

    image_bytes = await file.read()

    # Run palm analysis
    result = PalmAnalysisService.analyze_palm(
        image_bytes
    )

    # Store latest result in shared state
    state.latest_palm_analysis = result

    return result


@router.get(
    "/latest",
    summary="Get Latest Palm Analysis"
)
def get_latest_palm_analysis():
    """
    Return the latest palm analysis result.
    """

    if state.latest_palm_analysis is None:

        return {
            "success": False,
            "message": "No palm analysis available."
        }

    return state.latest_palm_analysis