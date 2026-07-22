from pydantic import BaseModel


class TarotResponse(BaseModel):
    success: bool
    card: dict