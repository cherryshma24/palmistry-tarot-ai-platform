from datetime import datetime


class ReportService:
    """
    Generate Palmistry, Tarot, or Combined reports.

    The report uses only the data that was actually
    supplied by the user.

    Palm report:
        Palm only

    Tarot report:
        Tarot only

    Combined report:
        Palm + previously selected Tarot reading
    """

    def generate_report(
        self,
        palm_result=None,
        tarot_result=None,
        report_type="palm"
    ):
        """
        Generate the requested report type.

        report_type:
            - palm
            - tarot
            - combined
        """

        # =====================================================
        # VALIDATE REPORT TYPE
        # =====================================================

        allowed_types = {
            "palm",
            "tarot",
            "combined"
        }

        if report_type not in allowed_types:

            raise ValueError(
                "Invalid report type. "
                "Use 'palm', 'tarot', or 'combined'."
            )

        # =====================================================
        # VALIDATE REQUIRED DATA
        # =====================================================

        if report_type == "palm" and palm_result is None:

            raise ValueError(
                "No palm analysis available."
            )

        if report_type == "tarot" and tarot_result is None:

            raise ValueError(
                "No Tarot reading available."
            )

        if report_type == "combined":

            if palm_result is None:

                raise ValueError(
                    "Palm analysis is required for a combined report."
                )

            if tarot_result is None:

                raise ValueError(
                    "Tarot reading is required for a combined report."
                )

        # =====================================================
        # PALM ANALYSIS
        # =====================================================

        palm_analysis = None

        if palm_result is not None:

            features = palm_result.get(
                "features",
                {}
            )

            line_detection = palm_result.get(
                "line_detection",
                features.get(
                    "line_detection",
                    {}
                )
            )

            palm_shape = palm_result.get(
                "palm_shape",
                features.get(
                    "palm_shape",
                    {}
                )
            )

            reading = palm_result.get(
                "reading",
                {}
            )

            # -------------------------------------------------
            # COUNT DETECTED LINES
            # -------------------------------------------------

            detected_lines = []

            for name, data in line_detection.items():

                if (
                    isinstance(data, dict)
                    and data.get(
                        "detected",
                        False
                    )
                ):

                    detected_lines.append(
                        name.title()
                    )

            total_lines = len(
                detected_lines
            )

            # -------------------------------------------------
            # LINE CONFIDENCE
            # -------------------------------------------------

            line_confidence = {}

            for name, data in line_detection.items():

                if isinstance(data, dict):

                    line_confidence[name] = data.get(
                        "confidence_percent",
                        0
                    )

            # -------------------------------------------------
            # AVERAGE CONFIDENCE
            # -------------------------------------------------

            confidence_values = list(
                line_confidence.values()
            )

            if confidence_values:

                average_confidence = round(
                    sum(confidence_values)
                    / len(confidence_values),
                    1
                )

            else:

                average_confidence = 0

            # -------------------------------------------------
            # OVERALL CV CONFIDENCE
            # -------------------------------------------------

            overall_cv_confidence = features.get(
                "analysis_confidence",
                features.get(
                    "yolo_line_confidence",
                    0
                )
            )

            # Convert 0-1 → percentage
            if (
                isinstance(
                    overall_cv_confidence,
                    (int, float)
                )
                and overall_cv_confidence <= 1
            ):

                overall_cv_confidence *= 100

            overall_cv_confidence = round(
                overall_cv_confidence,
                1
            )

            # -------------------------------------------------
            # LINE MEASUREMENTS
            # -------------------------------------------------

            line_lengths = {}
            line_angles = {}
            line_curvatures = {}

            for name, data in line_detection.items():

                if not isinstance(data, dict):
                    continue

                line_lengths[name] = data.get(
                    "length_pixels",
                    0
                )

                line_angles[name] = data.get(
                    "angle_degrees",
                    0
                )

                line_curvatures[name] = data.get(
                    "average_curvature_degrees",
                    0
                )

            # -------------------------------------------------
            # PALM SUMMARY
            # -------------------------------------------------

            palm_summary = (
                f"Computer vision detected "
                f"{total_lines} major palm lines "
                f"with an overall detection confidence "
                f"of {overall_cv_confidence}%."
            )

            palm_analysis = {

                "summary":
                    palm_summary,

                "analytics": {

                    "available":
                        True,

                    "status":
                        "Palm analysis data successfully included.",

                    "total_lines_detected":
                        total_lines,

                    "detected_lines":
                        detected_lines,

                    "average_line_confidence":
                        average_confidence,

                    "overall_cv_confidence":
                        overall_cv_confidence,

                    "line_confidence":
                        line_confidence,

                    "line_lengths":
                        line_lengths,

                    "line_angles":
                        line_angles,

                    "line_curvatures":
                        line_curvatures
                },

                "palm_shape":
                    palm_shape,

                "reading":
                    reading,

                "personality":
                    palm_result.get(
                        "personality",
                        {}
                    ),

                "total_landmarks":
                    palm_result.get(
                        "total_landmarks",
                        0
                    )
            }

        # =====================================================
        # TAROT ANALYSIS
        # =====================================================

        tarot_reading = None
        tarot_analytics = None

        if tarot_result is not None:

            tarot_reading = tarot_result

            # -------------------------------------------------
            # SINGLE CARD
            # -------------------------------------------------

            if tarot_result.get(
                "spread"
            ) == "Single Card":

                tarot_card = tarot_result.get(
                    "card",
                    {}
                )

                tarot_analytics = {

                    "available":
                        True,

                    "spread":
                        "Single Card",

                    "cards": [
                        tarot_card.get(
                            "name",
                            "Unknown"
                        )
                    ],

                    "card_count":
                        1
                }

            # -------------------------------------------------
            # THREE CARD
            # -------------------------------------------------

            else:

                cards = tarot_result.get(
                    "cards",
                    {}
                )

                card_names = []

                if isinstance(cards, dict):

                    for position in [
                        "past",
                        "present",
                        "future"
                    ]:

                        card = cards.get(
                            position,
                            {}
                        )

                        if isinstance(
                            card,
                            dict
                        ):

                            card_names.append(
                                card.get(
                                    "name",
                                    "Unknown"
                                )
                            )

                tarot_analytics = {

                    "available":
                        True,

                    "spread":
                        tarot_result.get(
                            "spread",
                            "Tarot"
                        ),

                    "cards":
                        card_names,

                    "card_count":
                        len(card_names)
                }

        # =====================================================
        # OVERALL GUIDANCE
        # =====================================================

        if report_type == "palm":

            overall_guidance = (
                "This report contains computer-vision "
                "palm analysis, AI-powered palmistry "
                "interpretation, and personality insights. "
                "These results are intended for "
                "entertainment and self-reflection."
            )

        elif report_type == "tarot":

            overall_guidance = (
                "This report contains Tarot guidance "
                "based on the Tarot reading selected "
                "by the user. The interpretation is "
                "intended for entertainment and "
                "self-reflection."
            )

        else:

            overall_guidance = (
                "This report combines the user's "
                "palm analysis with the Tarot reading "
                "they selected. These results are "
                "intended for entertainment and "
                "self-reflection."
            )

        # =====================================================
        # FINAL REPORT
        # =====================================================

        return {

            "success":
                True,

            "generated_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "report_version":
                "5.0",

            "platform":
                "Palmistry & Tarot Intelligence Platform",

            "report_type":
                report_type,

            # Palm is included ONLY when supplied
            "palm_analysis":
                palm_analysis,

            # Tarot is included ONLY when supplied
            "tarot_reading":
                tarot_reading,

            "tarot_analytics":
                tarot_analytics,

            "overall_guidance":
                overall_guidance,

            "disclaimer":
                (
                    "Palmistry and Tarot interpretations "
                    "are provided for entertainment and "
                    "self-reflection. They should not be "
                    "treated as scientific, medical, legal "
                    "or guaranteed predictions."
                )
        }