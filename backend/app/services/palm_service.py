import os
import math
import gc

from app.services.ai_manager import generate_palm_reading


# ============================================================
# YOLO MODEL
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

# YOLO model is loaded only when palm analysis is requested.
# This prevents YOLO/PyTorch from loading during FastAPI startup.
_model = None


def get_model():
    """
    Load YOLO model only once and only when required.

    This lazy-loading approach is useful for Render because
    PyTorch/Ultralytics does not need to be loaded during
    FastAPI startup.
    """

    global _model

    if _model is None:

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Palm YOLO model not found:\n"
                f"{MODEL_PATH}\n\n"
                "Copy best.pt into backend/models/palm_pose/"
            )

        print(
            f"Loading palm model: {MODEL_PATH}"
        )

        # Lazy import:
        # Prevents Ultralytics/PyTorch from being imported
        # while FastAPI is starting.
        from ultralytics import YOLO

        try:

            _model = YOLO(MODEL_PATH)

            # Put the underlying PyTorch model into evaluation mode.
            try:
                _model.model.eval()
            except Exception:
                pass

            print(
                "Palm YOLO model loaded successfully."
            )

        except Exception as e:

            print(
                "❌ Failed to load Palm YOLO model:"
            )
            print(e)

            # Make sure a failed model does not remain
            # partially initialized.
            _model = None

            gc.collect()

            raise

    return _model


# ============================================================
# PALM LINE ANALYSIS
# ============================================================

def analyze_palm_image(image_path):
    """
    Run YOLO palm-line detection and extract:

    - confidence
    - keypoints
    - line length
    - start/end points
    - angle
    - average curvature

    Optimized for low-memory CPU deployment.
    """

    import torch

    model = get_model()

    if not os.path.exists(image_path):
        raise FileNotFoundError(
            f"Palm image not found: {image_path}"
        )

    print("\n========================================")
    print("PALM ANALYSIS")
    print("========================================")
    print(f"Image: {image_path}")

    # ========================================================
    # CLASS NAMES
    # ========================================================

    class_names = {
        0: "fate",
        1: "head",
        2: "heart",
        3: "life"
    }

    # ========================================================
    # INITIALIZE PALM LINES
    # ========================================================

    palm_lines = {}

    for name in class_names.values():

        palm_lines[name] = {
            "detected": False,
            "confidence": 0.0,
            "confidence_percent": 0.0,
            "length_pixels": 0.0,
            "start_point": None,
            "end_point": None,
            "angle_degrees": 0.0,
            "average_curvature_degrees": 0.0,
            "keypoint_count": 0
        }

    results = None
    result = None

    # ========================================================
    # YOLO INFERENCE
    # ========================================================

    try:

        print(
            "Running YOLO inference on CPU..."
        )

        # torch.inference_mode() prevents gradient
        # calculations and reduces memory usage.
        with torch.inference_mode():

            results = model.predict(
                source=image_path,

                # Lower resolution reduces CPU/RAM usage.
                imgsz=416,

                # Existing confidence threshold.
                conf=0.05,

                # Explicit CPU inference for Render.
                device="cpu",

                # Prevent unnecessary console output.
                verbose=False,

                # Limit detections to avoid excessive
                # result objects.
                max_det=10
            )

        print(
            "YOLO inference completed."
        )

        if not results:
            raise RuntimeError(
                "YOLO returned no results."
            )

        result = results[0]

        # ====================================================
        # NO DETECTIONS
        # ====================================================

        if (
            result.boxes is None
            or len(result.boxes) == 0
        ):

            print(
                "No palm lines detected."
            )

            return {
                "palm_lines": palm_lines,
                "overall_confidence": 0.0
            }

        # ====================================================
        # BOXES / KEYPOINTS
        # ====================================================

        boxes = result.boxes
        keypoints = result.keypoints

        # ====================================================
        # PROCESS DETECTIONS
        # ====================================================

        for i in range(len(boxes)):

            # ------------------------------------------------
            # Class
            # ------------------------------------------------

            class_id = int(
                boxes.cls[i].item()
            )

            if class_id not in class_names:
                continue

            line_name = class_names[class_id]

            # ------------------------------------------------
            # Confidence
            # ------------------------------------------------

            confidence = float(
                boxes.conf[i].item()
            )

            # Keep only the BEST detection for
            # each palm line.
            if (
                palm_lines[line_name]["detected"]
                and confidence
                <= palm_lines[line_name]["confidence"]
            ):
                continue

            palm_lines[line_name][
                "detected"
            ] = True

            palm_lines[line_name][
                "confidence"
            ] = confidence

            palm_lines[line_name][
                "confidence_percent"
            ] = round(
                confidence * 100,
                1
            )

            # =================================================
            # KEYPOINTS
            # =================================================

            if keypoints is None:
                continue

            try:

                points = (
                    keypoints.xy[i]
                    .detach()
                    .cpu()
                    .numpy()
                )

            except Exception as e:

                print(
                    f"Keypoint extraction failed "
                    f"for {line_name}: {e}"
                )

                continue

            if (
                points is None
                or len(points) == 0
            ):
                continue

            # -------------------------------------------------
            # Remove invalid keypoints
            # -------------------------------------------------

            valid_points = []

            for point in points:

                x = float(point[0])
                y = float(point[1])

                if x > 0 and y > 0:

                    valid_points.append(
                        (x, y)
                    )

            if len(valid_points) < 2:
                continue

            palm_lines[line_name][
                "keypoint_count"
            ] = len(valid_points)

            # =================================================
            # START / END POINT
            # =================================================

            start_x, start_y = valid_points[0]
            end_x, end_y = valid_points[-1]

            palm_lines[line_name][
                "start_point"
            ] = {
                "x": round(
                    start_x,
                    2
                ),
                "y": round(
                    start_y,
                    2
                )
            }

            palm_lines[line_name][
                "end_point"
            ] = {
                "x": round(
                    end_x,
                    2
                ),
                "y": round(
                    end_y,
                    2
                )
            }

            # =================================================
            # LINE LENGTH
            # =================================================

            total_length = 0.0

            for j in range(
                1,
                len(valid_points)
            ):

                x1, y1 = valid_points[j - 1]
                x2, y2 = valid_points[j]

                distance = (
                    (x2 - x1) ** 2
                    +
                    (y2 - y1) ** 2
                ) ** 0.5

                total_length += distance

            palm_lines[line_name][
                "length_pixels"
            ] = round(
                total_length,
                2
            )

            # =================================================
            # OVERALL ANGLE
            # =================================================

            dx = end_x - start_x
            dy = end_y - start_y

            angle = math.degrees(
                math.atan2(
                    dy,
                    dx
                )
            )

            if angle < 0:
                angle += 360

            palm_lines[line_name][
                "angle_degrees"
            ] = round(
                angle,
                2
            )

            # =================================================
            # AVERAGE CURVATURE
            # =================================================

            angles = []

            for j in range(
                1,
                len(valid_points) - 1
            ):

                x1, y1 = valid_points[j - 1]
                x2, y2 = valid_points[j]
                x3, y3 = valid_points[j + 1]

                angle1 = math.degrees(
                    math.atan2(
                        y2 - y1,
                        x2 - x1
                    )
                )

                angle2 = math.degrees(
                    math.atan2(
                        y3 - y2,
                        x3 - x2
                    )
                )

                difference = abs(
                    angle2 - angle1
                )

                if difference > 180:
                    difference = (
                        360 - difference
                    )

                angles.append(
                    difference
                )

            if angles:

                palm_lines[line_name][
                    "average_curvature_degrees"
                ] = round(
                    sum(angles)
                    / len(angles),
                    2
                )

        # ====================================================
        # OVERALL CONFIDENCE
        # ====================================================

        detected_confidences = [
            data["confidence"]
            for data in palm_lines.values()
            if data["detected"]
        ]

        if detected_confidences:

            overall_confidence = (
                sum(
                    detected_confidences
                )
                /
                len(
                    detected_confidences
                )
            )

        else:

            overall_confidence = 0.0

        # ====================================================
        # PRINT RESULTS
        # ====================================================

        print("\n========================================")
        print("BEST PALM LINE DETECTIONS")
        print("========================================")

        for name, data in palm_lines.items():

            print(
                f"{name.upper():<6} -> "
                f"{data['confidence_percent']:.1f}%"
            )

        print(
            f"Overall confidence -> "
            f"{overall_confidence * 100:.1f}%"
        )

        print(
            "========================================\n"
        )

        # ====================================================
        # RETURN
        # ====================================================

        return {
            "palm_lines": palm_lines,
            "overall_confidence": round(
                overall_confidence,
                4
            )
        }

    finally:

        # ====================================================
        # MEMORY CLEANUP
        # ====================================================

        try:
            del results
        except Exception:
            pass

        try:
            del result
        except Exception:
            pass

        try:
            gc.collect()
        except Exception:
            pass

        # Render is CPU-only, but this is harmless if
        # CUDA is available in another environment.
        try:

            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        except Exception:
            pass


# ============================================================
# AI PALM READING
# ============================================================

def generate_reading(
    profile,
    palm_analysis
):
    """
    Send extracted palm features to the AI engine.
    """

    palm_features = {
        "line_detection": palm_analysis[
            "palm_lines"
        ],
        "analysis_confidence": palm_analysis[
            "overall_confidence"
        ]
    }

    print(
        "\nSending palm features to AI..."
    )

    reading = generate_palm_reading(
        profile,
        palm_features
    )

    return reading


# ============================================================
# COMPLETE PALM ANALYSIS
# ============================================================

def analyze_palm(
    image_path,
    profile=None
):
    """
    Complete palm analysis pipeline:

    Image
      ↓
    YOLO Palm Line Detection
      ↓
    Feature Extraction
      ↓
    OpenRouter AI Reading
      ↓
    Final Result
    """

    if profile is None:
        profile = {}

    print(
        "\n========== PALM ANALYSIS STARTED =========="
    )

    # ========================================================
    # STEP 1: COMPUTER VISION
    # ========================================================

    palm_analysis = analyze_palm_image(
        image_path
    )

    # ========================================================
    # STEP 2: AI INTERPRETATION
    # ========================================================

    try:

        reading = generate_reading(
            profile,
            palm_analysis
        )

    except Exception as e:

        print(
            f"AI reading failed: {e}"
        )

        reading = {
            "error": str(e)
        }

    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return {
        "success": True,
        "image_path": image_path,
        "palm_analysis": palm_analysis,
        "reading": reading
    }