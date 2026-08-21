import os
from typing import Dict, Any

from ultralytics import YOLO


# ============================================================
# YOLO MODEL PATH
# ============================================================

MODEL_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "models",
        "palm_pose",
        "best.pt"
    )
)


# ============================================================
# MODEL LOADER
# ============================================================

_model = None


def _load_model():
    """
    Load YOLO model only when palm analysis is requested.
    This avoids loading the model during application startup.
    """

    global _model

    if _model is not None:
        return _model

    if not os.path.exists(MODEL_PATH):
        print(
            f"YOLO model not found: {MODEL_PATH}"
        )
        return None

    try:
        print(
            f"Loading YOLO palm model: {MODEL_PATH}"
        )

        _model = YOLO(MODEL_PATH)

        print("YOLO palm model loaded successfully.")

        return _model

    except Exception as e:
        print(
            f"YOLO model loading error: {e}"
        )

        return None


# ============================================================
# SAFE NUMBER
# ============================================================

def _safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


# ============================================================
# PALM LINE ANALYSIS
# ============================================================

def analyze_palm_image(image) -> Dict[str, Any]:
    """
    Analyze palm image using the trained YOLO pose model.

    Expected classes:
        fate
        head
        heart
        life

    Returns a stable structure that can safely be consumed
    by PalmAnalysisService.
    """

    result = {
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

    # --------------------------------------------------------
    # LOAD MODEL
    # --------------------------------------------------------

    model = _load_model()

    if model is None:
        print(
            "YOLO model unavailable. Returning empty detection."
        )
        return result

    # --------------------------------------------------------
    # RUN YOLO
    # --------------------------------------------------------

    try:

        predictions = model.predict(
            source=image,
            conf=0.10,
            verbose=False
        )

        if not predictions:
            return result

        prediction = predictions[0]

        # ----------------------------------------------------
        # CLASS NAMES
        # ----------------------------------------------------

        names = prediction.names

        if not names:
            return result

        # ----------------------------------------------------
        # DETECTIONS
        # ----------------------------------------------------

        if prediction.boxes is None:
            return result

        boxes = prediction.boxes

        confidences = []

        for index in range(len(boxes)):

            confidence = _safe_float(
                boxes.conf[index].item()
            )

            class_id = int(
                boxes.cls[index].item()
            )

            class_name = names.get(
                class_id,
                ""
            )

            class_name = str(
                class_name
            ).lower().strip()

            # ------------------------------------------------
            # ONLY EXPECTED PALM LINE CLASSES
            # ------------------------------------------------

            if class_name not in result["palm_lines"]:
                continue

            line = result["palm_lines"][class_name]

            # ------------------------------------------------
            # Keep strongest detection for each line
            # ------------------------------------------------

            if confidence >= line["confidence"]:

                line["detected"] = True

                line["confidence"] = round(
                    confidence,
                    4
                )

                line["confidence_percent"] = round(
                    confidence * 100,
                    1
                )

            confidences.append(
                confidence
            )

        # ----------------------------------------------------
        # POSE KEYPOINT DATA
        # ----------------------------------------------------

        if (
            hasattr(prediction, "keypoints")
            and prediction.keypoints is not None
        ):

            keypoints = prediction.keypoints

            # Some YOLO pose outputs contain
            # keypoint coordinates.
            #
            # We don't overwrite the existing
            # confidence values here because the
            # detector confidence is already stored
            # above.

            print(
                "YOLO pose keypoints detected."
            )

        # ----------------------------------------------------
        # OVERALL CONFIDENCE
        # ----------------------------------------------------

        detected_confidences = [
            line["confidence"]
            for line in result["palm_lines"].values()
            if line["detected"]
        ]

        if detected_confidences:

            result["overall_confidence"] = round(
                sum(detected_confidences)
                / len(detected_confidences),
                4
            )

        return result

    except Exception as e:

        print(
            f"YOLO palm analysis error: {e}"
        )

        return result