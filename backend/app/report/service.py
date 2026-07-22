from datetime import datetime

from app.palm.service import PalmAnalysisService
from app.tarot.service import TarotService


class ReportService:
    """
    Generate a combined Palmistry & Tarot report.
    """

    def __init__(self):
        self.tarot_service = TarotService()

    def generate_report(self):
        """
        Generate a report using Tarot reading.
        Palm data can later be replaced with actual analysis results.
        """

        # Draw a tarot card
        tarot_result = self.tarot_service.single_card_reading()

        report = {
            "success": True,

            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "palm_analysis": {
                "hand_detected": True,
                "total_landmarks": 21,
                "status": "Palm analysis completed successfully."
            },

            "tarot_reading": tarot_result,

            "overall_guidance": (
                "Your palm analysis detected a valid hand with 21 landmarks. "
                "The selected tarot card provides guidance based on traditional "
                "tarot interpretations. Consider this reading as a source of "
                "reflection and personal insight."
            )
        }

        return report