from pydantic import BaseModel
from typing import List, Optional


class Landmark(BaseModel):
    x: float
    y: float
    z: float


class PalmAnalysisResponse(BaseModel):
    success: bool
    message: str
    total_landmarks: int
    landmarks: Optional[List[Landmark]] = None