import os
import tempfile

from app.services.palm_service import analyze_palm_image

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

        print("========== STEP 1 : PREPROCESS IMAGE ==========")

        _, rgb_image = preprocess_image(image_bytes)

        print("✅ Image preprocessing completed.")

        # =====================================================
        # STEP 2 : ENHANCE IMAGE
        # =====================================================

        print("\n========== STEP 2 : ENHANCE IMAGE ==========")

        try:
            enhanced_image = enhance_palm_image(rgb_image)

            if enhanced_image is not None:
                print("✅ Palm image enhancement completed.")
            else:
                print("⚠️ Image enhancement returned None.")

        except Exception as e:
            print("⚠️ Image enhancement failed:")
            print(f"{type(e).__name__}: {e}")

            # Enhancement is not required for YOLO,
            # so continue processing.
            enhanced_image = rgb_image

        # =====================================================
        # STEP 3 : HAND LANDMARK DETECTION
        # =====================================================

        print("\n========== STEP 3 : HAND LANDMARK DETECTION ==========")

        try:

            landmarks = detect_hand_landmarks(rgb_image)

            if landmarks is not None:
                print("✅ MediaPipe hand landmarks detected.")

                try:
                    print(
                        f"Total landmarks: {len(landmarks)}"
                    )
                except Exception:
                    pass

            else:
                print("⚠️ MediaPipe hand not detected.")

        except Exception as e:

            print("❌ MediaPipe detection failed.")

            print(
                f"{type(e).__name__}: {e}"
            )

            landmarks = None

        # =====================================================
        # STEP 4 : REAL YOLO PALM LINE DETECTION
        # =====================================================

        print(
            "\n========== STEP 4 : REAL YOLO PALM LINE DETECTION ==========\n"
        )

        temp_image_path = None

        try:

            # -------------------------------------------------
            # Create temporary image
            # -------------------------------------------------

            with tempfile.NamedTemporaryFile(
                suffix=".jpg",
                delete=False
            ) as temp_file:

                temp_file.write(image_bytes)

                temp_image_path = temp_file.name

            print(
                f"Temporary palm image: {temp_image_path}"
            )

            print("\n🔥 Calling REAL YOLO palm detector...")

            # -------------------------------------------------
            # Run existing YOLO service
            # -------------------------------------------------

            yolo_analysis = analyze_palm_image(
                temp_image_path
            )

            # -------------------------------------------------
            # Print raw YOLO response
            # -------------------------------------------------

            print("\n🔥 RAW YOLO RESULT:")
            print("----------------------------------------")
            print(yolo_analysis)
            print("----------------------------------------")

            print(
                "\n✅ Real YOLO analysis completed."
            )

        except Exception as e:

            # -------------------------------------------------
            # DO NOT silently convert error into 0%
            # -------------------------------------------------

            print("\n❌ YOLO ANALYSIS FAILED")

            print("----------------------------------------")

            print(
                f"ERROR TYPE: {type(e).__name__}"
            )

            print(
                f"ERROR MESSAGE: {e}"
            )

            print("----------------------------------------")

            # Re-raise the error so we can see
            # the real problem during debugging.
            raise

        finally:

            # -------------------------------------------------
            # Delete temporary image
            # -------------------------------------------------

            if (
                temp_image_path is not None
                and os.path.exists(temp_image_path)
            ):

                try:

                    os.remove(
                        temp_image_path
                    )

                    print(
                        "✅ Temporary image deleted."
                    )

                except Exception as e:

                    print(
                        f"⚠️ Could not delete temporary image: {e}"
                    )

        # =====================================================
        # STEP 5 : YOLO LINE DATA
        # =====================================================

        print(
            "\n========== STEP 5 : YOLO PALM LINE RESULTS ==========\n"
        )

        palm_lines = yolo_analysis.get(
            "palm_lines",
            {}
        )

        overall_confidence = yolo_analysis.get(
            "overall_confidence",
            0.0
        )

        # -----------------------------------------------------
        # Print every detected line
        # -----------------------------------------------------

        for name, data in palm_lines.items():

            detected = data.get(
                "detected",
                False
            )

            confidence = data.get(
                "confidence",
                0.0
            )

            confidence_percent = data.get(
                "confidence_percent",
                confidence * 100
            )

            print(
                f"{name.upper():<8} -> "
                f"Detected: {detected} | "
                f"Confidence: {confidence:.4f} | "
                f"Percentage: {confidence_percent:.1f}%"
            )

        print(
            "\nOverall YOLO confidence -> "
            f"{overall_confidence * 100:.1f}%"
        )

        # =====================================================
        # STEP 6 : HAND FEATURES
        # =====================================================

        print(
            "\n========== STEP 6 : PALM FEATURE EXTRACTION ==========\n"
        )

        if landmarks is not None:

            print(
                "Using MediaPipe + OpenCV + YOLO"
            )

            # -------------------------------------------------
            # Extract palm features
            # -------------------------------------------------

            try:

                features = extract_palm_features(
                    landmarks
                )

                print(
                    "✅ Palm features extracted."
                )

            except Exception as e:

                print(
                    "⚠️ Palm feature extraction failed:"
                )

                print(
                    f"{type(e).__name__}: {e}"
                )

                features = {}

            # -------------------------------------------------
            # Palm shape
            # -------------------------------------------------

            try:

                palm_shape = classify_palm_shape(
                    landmarks
                )

                print(
                    f"✅ Palm shape: {palm_shape}"
                )

            except Exception as e:

                print(
                    "⚠️ Palm shape classification failed:"
                )

                print(
                    f"{type(e).__name__}: {e}"
                )

                palm_shape = "Unknown"

            features["palm_shape"] = palm_shape

        else:

            print(
                "⚠️ MediaPipe hand not detected."
            )

            features = {}

            palm_shape = "Unknown"

        # =====================================================
        # STEP 7 : ADD YOLO INFORMATION
        # =====================================================

        print(
            "\n========== STEP 7 : ADDING YOLO FEATURES ==========\n"
        )

        # -----------------------------------------------------
        # Complete palm-line information
        # -----------------------------------------------------

        features["line_detection"] = palm_lines

        # -----------------------------------------------------
        # Overall YOLO confidence
        # -----------------------------------------------------

        features["yolo_line_confidence"] = (
            overall_confidence
        )

        features["analysis_confidence"] = (
            overall_confidence
        )

        # -----------------------------------------------------
        # System information
        # -----------------------------------------------------

        features["analysis_version"] = "3.0"

        features["cv_engine"] = (
            "MediaPipe + OpenCV + YOLO"
        )

        features["analysis_type"] = (
            "Palmistry Intelligence"
        )

        features["ai_provider"] = (
            "OpenRouter"
        )

        # -----------------------------------------------------
        # Detected line names
        # -----------------------------------------------------

        features["detected_lines"] = [

            name.title()

            for name, data in palm_lines.items()

            if data.get("detected", False)

        ]

        print(
            "\nDetected lines:"
        )

        print(
            features["detected_lines"]
        )

        # =====================================================
        # STEP 8 : PROFILE
        # =====================================================

        profile = {

            "full_name": "Guest",

            "age": "Unknown",

            "gender": "Unknown",

            "occupation": "Unknown",

            "interest": "General"

        }

        # =====================================================
        # STEP 9 : AI BYPASS
        # =====================================================

        print(
            "\n========== STEP 9 : AI READING ==========\n"
        )

        # -----------------------------------------------------
        # AI temporarily bypassed
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
                overall_confidence

        }

        print(
            "OpenRouter AI temporarily bypassed "
            "for Render testing."
        )

        # =====================================================
        # STEP 10 : PERSONALITY AI BYPASS
        # =====================================================

        print(
            "\n========== STEP 10 : PERSONALITY ==========\n"
        )

        personality = {

            "message":
                "Personality AI temporarily bypassed "
                "for Render testing.",

            "type":
                "General"

        }

        print(
            "Personality AI temporarily bypassed "
            "for Render testing."
        )

        # =====================================================
        # STEP 11 : FINAL RESPONSE
        # =====================================================

        print(
            "\n========== PALM ANALYSIS COMPLETED ==========\n"
        )

        return {

            "success":
                True,

            "system": {

                "version":
                    "3.0",

                "platform":
                    "Palmistry & Tarot Intelligence Platform",

                "cv_engine":
                    "MediaPipe + OpenCV + YOLO",

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

            # IMPORTANT:
            # Report frontend should read this field.
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