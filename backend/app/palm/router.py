from fastapi import APIRouter, UploadFile, File
from app.palm.service import PalmAnalysisService


router = APIRouter(
    prefix="/palm",
    tags=["Palm Analysis"]
)


@router.post("/analyze")
async def analyze_palm(file: UploadFile = File(...)):

    image_bytes = await file.read()

    result = PalmAnalysisService.analyze_palm(
        image_bytes
    )

    return result