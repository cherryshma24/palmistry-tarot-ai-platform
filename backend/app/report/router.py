from fastapi import APIRouter

from app.report.service import ReportService

router = APIRouter(
    prefix="/report",
    tags=["Report"]
)

report_service = ReportService()


@router.get("/generate", summary="Generate Palmistry & Tarot Report")
def generate_report():
    """
    Generate a combined Palmistry & Tarot report.
    """
    return report_service.generate_report()