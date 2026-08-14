from fastapi import APIRouter, HTTPException, Query

from app.report.service import ReportService
from app.palm import state

router = APIRouter(
    prefix="/report",
    tags=["Report"]
)

report_service = ReportService()


@router.post("/generate")
async def generate_report(
    report_type: str = Query(
        "palm",
        description="Report type: palm, tarot, or combined"
    )
):
    """
    Generate a report based on what the user actually selected.

    palm:
        Generates Palmistry report only.

    tarot:
        Generates Tarot report only using the selected/drawn Tarot data.

    combined:
        Generates Palmistry + Tarot report.
    """

    try:

        # =====================================================
        # VALIDATE REPORT TYPE
        # =====================================================

        allowed_types = {
            "palm",
            "tarot",
            "combined"
        }

        if report_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid report type. "
                    "Use 'palm', 'tarot', or 'combined'."
                )
            )

        # =====================================================
        # GET LATEST PALM ANALYSIS
        # =====================================================

        palm_result = getattr(
            state,
            "latest_palm_analysis",
            None
        )

        # =====================================================
        # GET LATEST TAROT RESULT
        # =====================================================

        tarot_result = getattr(
            state,
            "latest_tarot_reading",
            None
        )

        # =====================================================
        # PALM REPORT
        # =====================================================

        if report_type == "palm":

            if palm_result is None:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "No palm analysis available. "
                        "Please analyze a palm image first."
                    )
                )

            return report_service.generate_report(
                palm_result=palm_result,
                tarot_result=None,
                report_type="palm"
            )

        # =====================================================
        # TAROT REPORT
        # =====================================================

        if report_type == "tarot":

            if tarot_result is None:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "No Tarot reading available. "
                        "Please select a Tarot reading first."
                    )
                )

            return report_service.generate_report(
                palm_result=None,
                tarot_result=tarot_result,
                report_type="tarot"
            )

        # =====================================================
        # COMBINED REPORT
        # =====================================================

        if report_type == "combined":

            if palm_result is None:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "No palm analysis available. "
                        "Please analyze a palm image first."
                    )
                )

            if tarot_result is None:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "No Tarot reading available. "
                        "Please select a Tarot reading first."
                    )
                )

            return report_service.generate_report(
                palm_result=palm_result,
                tarot_result=tarot_result,
                report_type="combined"
            )

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Report generation failed: {str(e)}"
        )