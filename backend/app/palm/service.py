from app.palm.utils import preprocess_image
from app.palm.detector import detect_hand_landmarks
from app.palm.features import extract_palm_features
from app.services.gemini_service import generate_palm_reading
from app.palm.image_enhancer import enhance_palm_image
from app.palm.line_detector import detect_palm_lines
from app.palm.shape_classifier import classify_palm_shape


class PalmAnalysisService:

    @staticmethod
    def analyze_palm(image_bytes: bytes):
        print("========== SERVICE.PY RUNNING ==========")
        # Step 1: Preprocess image
        _, rgb_image = preprocess_image(image_bytes)


        # Step 2: Enhance image
        enhanced_image = enhance_palm_image(rgb_image)


        # Step 3: Detect landmarks
        landmarks = detect_hand_landmarks(rgb_image)


        # Step 4: Detect palm lines
        candidate_lines = detect_palm_lines(enhanced_image)


        if landmarks is None:
            return {
                "success": False,
                "message": "No hand detected.",
                "total_landmarks": 0,
                "landmarks": []
            }


        # Step 5: Extract features
        features = extract_palm_features(landmarks)


        # Step 6: Palm shape classification
        palm_shape = classify_palm_shape(landmarks)


        # Step 7: Line information
        line_detection = {

            "candidate_lines_detected": len(candidate_lines),

            "estimated_main_lines": min(5, len(candidate_lines)),

            "line_quality": (
                "Excellent"
                if len(candidate_lines) > 150
                else "Good"
                if len(candidate_lines) > 80
                else "Moderate"
                if len(candidate_lines) > 40
                else "Low"
            ),

            "status": "Palm line candidates extracted successfully."
        }


        # Step 8: Add extra data for Gemini
        features["palm_shape"] = palm_shape
        features["line_detection"] = line_detection


        # Step 9: Gemini AI reading

        print("========== BEFORE GEMINI ==========")
        profile = {
            "age": "Unknown",
            "gender": "Unknown",
            "interest": "General"
        }


        reading = generate_palm_reading(
            profile,
            features
        )

        print("========== AFTER GEMINI ==========")


        return {

            "success": True,

            "message": "Palm analysis completed successfully.",

            "total_landmarks": len(landmarks),

            "features": features,

            "palm_shape": palm_shape,

            "line_detection": line_detection,

            "reading": reading,

            "landmarks": landmarks
        }