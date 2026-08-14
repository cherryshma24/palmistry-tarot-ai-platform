from app.palm.utils import preprocess_image
from app.palm.detector import detect_hand_landmarks
from app.palm.features import extract_palm_features
from app.services.ai_manager import generate_palm_reading
from app.services.personality_service import generate_personality_profile
from app.palm.image_enhancer import enhance_palm_image
from app.palm.shape_classifier import classify_palm_shape

# NEW: trained YOLO palm-line model
from app.services.palm_service import analyze_palm_image


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
        # STEP 4 : YOLO PALM LINE DETECTION
        # =====================================================

        # Save image temporarily because the YOLO service
        # works with an image path.
        import os
        import tempfile
        import cv2

        temp_path = None

        try:

            with tempfile.NamedTemporaryFile(
                suffix=".jpg",
                delete=False
            ) as temp_file:

                temp_path = temp_file.name

            # enhanced_image is RGB, convert to BGR for OpenCV
            bgr_image = cv2.cvtColor(
                enhanced_image,
                cv2.COLOR_RGB2BGR
            )

            cv2.imwrite(
                temp_path,
                bgr_image
            )

            # Run trained YOLO model
            yolo_analysis = analyze_palm_image(
                temp_path
            )

        finally:

            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

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

        print("\n========== YOLO PALM LINE RESULTS ==========\n")

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
                "Using MediaPipe Hand Detection + YOLO Palm Lines"
            )

            features = extract_palm_features(
                landmarks
            )

            palm_shape = classify_palm_shape(
                landmarks
            )

            features["palm_shape"] = palm_shape

            features["line_detection"] = palm_lines

            features["yolo_line_confidence"] = overall_confidence

            features["analysis_confidence"] = overall_confidence

            features["analysis_version"] = "3.0"

            features["cv_engine"] = (
                "MediaPipe + OpenCV + YOLOv8 Pose"
            )

            features["analysis_type"] = (
                "Palmistry Intelligence"
            )

            features["ai_provider"] = "OpenRouter"

            features["detected_lines"] = [
    name.title()
    for name, data in palm_lines.items()
    if data.get("detected")
]

        else:

            print(
                "MediaPipe hand not detected. "
                "Using YOLO palm-line analysis."
            )

            features = {

                "palm_shape": "Unknown",

                "line_detection": palm_lines,

                "yolo_line_confidence":
                    overall_confidence,

                "analysis_confidence":
                    overall_confidence,

                "analysis_version": "3.0",

                "cv_engine":
                    "OpenCV + YOLOv8 Pose",

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
        # STEP 7 : SEND YOLO FEATURES TO AI
        # =====================================================

        print(
            "\n========== FEATURES SENT TO AI ==========\n"
        )

        print(features)

        reading = generate_palm_reading(
            profile,
            features
        )

        # =====================================================
        # STEP 8 : PERSONALITY PROFILE
        # =====================================================

        personality = generate_personality_profile(

            profile=profile,

            palm_reading=reading,

            tarot_reading=None

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

            "success": True,

            "system": {

                "version": "3.0",

                "platform":
                    "Palmistry & Tarot Intelligence Platform",

                "cv_engine":
                    "MediaPipe + OpenCV + YOLOv8 Pose",

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
                len(landmarks) if landmarks else 0,

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
                landmarks if landmarks else []

        }