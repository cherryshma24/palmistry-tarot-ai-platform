
import os
import math

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
    """

    global _model

    if _model is None:

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Palm YOLO model not found:\n{MODEL_PATH}\n\n"
                "Copy best.pt into backend/models/palm_pose/"
            )

        print(f"Loading palm model: {MODEL_PATH}")

        # Lazy import:
        # Prevents Ultralytics/PyTorch from being imported
        # while FastAPI is starting.
        from ultralytics import YOLO

        _model = YOLO(MODEL_PATH)

        print("Palm YOLO model loaded successfully.")

    return _model


# ============================================================
# PALM LINE ANALYSIS
# ============================================================

def analyze_palm_image(image_path):
    """
    Run YOLO palm-line detection and extract
    confidence, keypoints, length and angle information.
    """

    model = get_model()

    if not os.path.exists(image_path):
        raise FileNotFoundError(
            f"Palm image not found: {image_path}"
        )

    print("\n========================================")
    print("PALM ANALYSIS")
    print("========================================")
    print(f"Image: {image_path}")

    results = model.predict(
        source=image_path,
        conf=0.05,
        imgsz=640,
        device="cpu",
        verbose=False
    )

    if not results:
        raise RuntimeError("YOLO returned no results.")

    result = results[0]

    class_names = {
        0: "fate",
        1: "head",
        2: "heart",
        3: "life"
    }

    palm_lines = {}

    # Initialize all expected lines
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

    # --------------------------------------------------------
    # No detections
    # --------------------------------------------------------

    if result.boxes is None or len(result.boxes) == 0:

        print("No palm lines detected.")

        return {
            "palm_lines": palm_lines,
            "overall_confidence": 0.0
        }

    # --------------------------------------------------------
    # Process detections
    # --------------------------------------------------------

    boxes = result.boxes
    keypoints = result.keypoints

    for i in range(len(boxes)):

        class_id = int(boxes.cls[i].item())
        confidence = float(boxes.conf[i].item())

        if class_id not in class_names:
            continue

        line_name = class_names[class_id]

        # Keep the BEST detection for each line
        if (
            palm_lines[line_name]["detected"]
            and confidence <= palm_lines[line_name]["confidence"]
        ):
            continue

        palm_lines[line_name]["detected"] = True

        palm_lines[line_name]["confidence"] = confidence

        palm_lines[line_name]["confidence_percent"] = round(
            confidence * 100,
            1
        )

        # ----------------------------------------------------
        # Keypoints
        # ----------------------------------------------------

        if keypoints is None:
            continue

        try:
            points = keypoints.xy[i].cpu().numpy()
        except Exception:
            continue

        if points is None or len(points) == 0:
            continue

        # Remove invalid points
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

        palm_lines[line_name]["keypoint_count"] = len(
            valid_points
        )

        # ----------------------------------------------------
        # Start / End
        # ----------------------------------------------------

        start_x, start_y = valid_points[0]
        end_x, end_y = valid_points[-1]

        palm_lines[line_name]["start_point"] = {
            "x": round(start_x, 2),
            "y": round(start_y, 2)
        }

        palm_lines[line_name]["end_point"] = {
            "x": round(end_x, 2),
            "y": round(end_y, 2)
        }

        # ----------------------------------------------------
        # Length
        # ----------------------------------------------------

        total_length = 0.0

        for j in range(1, len(valid_points)):

            x1, y1 = valid_points[j - 1]
            x2, y2 = valid_points[j]

            distance = (
                (x2 - x1) ** 2 +
                (y2 - y1) ** 2
            ) ** 0.5

            total_length += distance

        palm_lines[line_name]["length_pixels"] = round(
            total_length,
            2
        )

        # ----------------------------------------------------
        # Overall angle
        # ----------------------------------------------------

        dx = end_x - start_x
        dy = end_y - start_y

        angle = math.degrees(
            math.atan2(dy, dx)
        )

        if angle < 0:
            angle += 360

        palm_lines[line_name]["angle_degrees"] = round(
            angle,
            2
        )

        # ----------------------------------------------------
        # Average curvature
        # ----------------------------------------------------

        angles = []

        for j in range(1, len(valid_points) - 1):

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
                difference = 360 - difference

            angles.append(difference)

        if angles:

            palm_lines[line_name][
                "average_curvature_degrees"
            ] = round(
                sum(angles) / len(angles),
                2
            )

    # ========================================================
    # Overall confidence
    # ========================================================

    detected_confidences = [
        data["confidence"]
        for data in palm_lines.values()
        if data["detected"]
    ]

    if detected_confidences:

        overall_confidence = (
            sum(detected_confidences)
            / len(detected_confidences)
        )

    else:

        overall_confidence = 0.0

    print("\n========================================")
    print("BEST PALM LINE DETECTIONS")
    print("========================================")

    for name, data in palm_lines.items():

        print(
            f"{name.upper():<6} -> "
            f"{data['confidence_percent']:.1f}%"
        )

    print("========================================\n")

    return {
        "palm_lines": palm_lines,
        "overall_confidence": round(
            overall_confidence,
            4
        )
    }


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
        "line_detection": palm_analysis["palm_lines"],
        "analysis_confidence": palm_analysis[
            "overall_confidence"
        ]
    }

    print("\nSending palm features to AI...")

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

    # --------------------------------------------------------
    # Step 1: Computer Vision
    # --------------------------------------------------------

    palm_analysis = analyze_palm_image(
        image_path
    )

    # --------------------------------------------------------
    # Step 2: AI Interpretation
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Final response
    # --------------------------------------------------------

    return {
        "success": True,
        "image_path": image_path,
        "palm_analysis": palm_analysis,
        "reading": reading
    }

