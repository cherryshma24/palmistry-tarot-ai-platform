from app.palm.utils import preprocess_image
from app.palm.detector import detect_hand_landmarks
from app.palm.features import extract_palm_features
from app.palm.image_enhancer import enhance_palm_image
from app.palm.shape_classifier import classify_palm_shape


class PalmAnalysisService:

    @staticmethod
    def analyze_palm(image_bytes: bytes):

        print("\n========== PALM ANALYSIS STARTED ==========\n")

        # =====================================================
        # STEP 1 : PREPROCESS IMAGE
        # =====================================================

        _, rgb_image = preprocess_image(image_bytes)

        # =====================================================
        # STEP 2 : ENHANCE IMAGE
        # =====================================================

        enhanced_image = enhance_palm_image(rgb_image)

        # =====================================================
        # STEP 3 : HAND LANDMARK DETECTION
        # =====================================================

        landmarks = detect_hand_landmarks(rgb_image)

        # =====================================================
        # STEP 4 : YOLO BYPASS
        # =====================================================

        # YOLO is temporarily disabled for Render testing.
        # This allows us to check whether the remaining
        # palm-analysis pipeline works correctly.

        yolo_analysis = {
            "palm_lines": {
                "fate": {
                    "detected": False,
                    "confidence": 0.0,
                    "confidence_percent": 0.0
                },
                "head": {
                    "detected": False,
                    "confidence": 0.0,
                    "confidence_percent": 0.0
                },
                "heart": {
                    "detected": False,
                    "confidence": 0.0,
                    "confidence_percent": 0.0
                },
                "life": {
                    "detected": False,
                    "confidence": 0.0,
                    "confidence_percent": 0.0
                }
            },
            "overall_confidence": 0.0
        }

        print(
            "YOLO temporarily bypassed for Render testing"
        )

        # =====================================================
        # YOLO LINE DATA
        # =====================================================

        palm_lines = yolo_analysis.get(
            "palm_lines",
            {}
        )

        overall_confidence = yolo_analysis.get(
            "overall_confidence",
            0.0
        )

        print(
            "\n========== YOLO PALM LINE RESULTS ==========\n"
        )

        for name, data in palm_lines.items():

            print(
                f"{name.upper():<6} -> "
                f"{data.get('confidence_percent', 0.0):.1f}%"
            )

        # =====================================================
        # STEP 5 : HAND FEATURES
        # =====================================================

        if landmarks is not None:

            print(
                "Using MediaPipe Hand Detection "
                "+ Palm Feature Extraction"
            )

            # Extract palm features

            features = extract_palm_features(
                landmarks
            )

            # Classify palm shape

            palm_shape = classify_palm_shape(
                landmarks
            )

            features["palm_shape"] = palm_shape

            # Palm-line information

            features["line_detection"] = palm_lines

            features["yolo_line_confidence"] = (
                overall_confidence
            )

            features["analysis_confidence"] = (
                overall_confidence
            )

            # System information

            features["analysis_version"] = "3.0"

            features["cv_engine"] = (
                "MediaPipe + OpenCV"
            )

            features["analysis_type"] = (
                "Palmistry Intelligence"
            )

            features["ai_provider"] = (
                "OpenRouter"
            )

            # Detected lines

            features["detected_lines"] = [
                name.title()
                for name, data in palm_lines.items()
                if data.get("detected")
            ]

        else:

            print(
                "MediaPipe hand not detected."
            )

            features = {

                "palm_shape": "Unknown",

                "line_detection": palm_lines,

                "yolo_line_confidence":
                    overall_confidence,

                "analysis_confidence":
                    overall_confidence,

                "analysis_version":
                    "3.0",

                "cv_engine":
                    "OpenCV",

                "analysis_type":
                    "Palmistry Intelligence",

                "ai_provider":
                    "OpenRouter",

                "detected_lines": [
                    name.title()
                    for name, data in palm_lines.items()
                    if data.get("detected")
                ]
            }

            palm_shape = "Unknown"

        # =====================================================
        # STEP 6 : PROFILE
        # =====================================================

        profile = {

            "full_name": "Guest",

            "age": "Unknown",

            "gender": "Unknown",

            "occupation": "Unknown",

            "interest": "General"

        }

        # =====================================================
        # STEP 7 : AI BYPASS
        # =====================================================

        print(
            "\n========== FEATURES SENT TO AI ==========\n"
        )

        print(features)

        # -----------------------------------------------------
        # OpenRouter temporarily bypassed
        # -----------------------------------------------------

        reading = {

            "message":
                "AI temporarily bypassed for Render testing.",

            "palm_analysis": {

                "palm_shape":
                    palm_shape,

                "detected_lines":
                    features.get(
                        "detected_lines",
                        []
                    ),

                "confidence":
                    features.get(
                        "analysis_confidence",
                        0.0
                    )
            },

            "confidence":
                0

        }

        print(
            "OpenRouter AI temporarily bypassed "
            "for Render testing"
        )

        # =====================================================
        # STEP 8 : PERSONALITY AI BYPASS
        # =====================================================

        personality = {

            "message":
                "Personality AI temporarily bypassed "
                "for Render testing.",

            "type":
                "General"

        }

        print(
            "Personality AI temporarily bypassed "
            "for Render testing"
        )

        print(
            "\n========== AI READING GENERATED ==========\n"
        )

        print(
            "\n========== PERSONALITY PROFILE GENERATED ==========\n"
        )

        # =====================================================
        # STEP 9 : FINAL RESPONSE
        # =====================================================

        return {

            "success":
                True,

            "system": {

                "version":
                    "3.0",

                "platform":
                    "Palmistry & Tarot Intelligence Platform",

                "cv_engine":
                    "MediaPipe + OpenCV",

                "ai_engine":
                    "OpenRouter",

                "analysis_engine":
                    "Palmistry Intelligence",

                "report_generator":
                    "AI Interpretation Service"

            },

            "message":
                "Palm analysis completed successfully.",

            "total_landmarks":
                len(landmarks)
                if landmarks
                else 0,

            "features":
                features,

            "palm_shape":
                palm_shape,

            "line_detection":
                palm_lines,

            "reading":
                reading,

            "personality":
                personality,

            "landmarks":
                landmarks
                if landmarks
                else []

        }