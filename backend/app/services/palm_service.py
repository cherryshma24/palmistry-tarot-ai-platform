
import os
import math
import gc
import time

# ============================================================
# RENDER / CPU OPTIMIZATION
# ============================================================

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

from app.services.ai_manager import generate_palm_reading


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
        "best.pt",
    )
)


# ============================================================
# GLOBAL MODEL
# ============================================================

_model = None


# ============================================================
# GET YOLO MODEL
# ============================================================

def get_model():

    global _model

    if _model is not None:
        return _model

    if not os.path.isfile(MODEL_PATH):

        raise FileNotFoundError(
            f"""
Palm YOLO model not found.

Expected location:
{MODEL_PATH}

Make sure this file exists:

backend/models/palm_pose/best.pt
"""
        )

    print()
    print("========================================")
    print("LOADING PALM YOLO MODEL")
    print("========================================")
    print(f"Model path: {MODEL_PATH}")

    import torch

    try:
        torch.set_num_threads(1)
    except Exception:
        pass

    try:
        torch.set_num_interop_threads(1)
    except Exception:
        pass

    from ultralytics import YOLO

    try:

        model = YOLO(MODEL_PATH)

        try:
            model.to("cpu")
        except Exception:
            pass

        try:
            model.model.eval()
        except Exception:
            pass

        _model = model

        print("✅ Palm YOLO model loaded successfully.")
        print("✅ Device: CPU")

        # ====================================================
        # IMPORTANT: PRINT MODEL CLASSES
        # ====================================================

        print()
        print("🔥 MODEL CLASS NAMES")
        print("----------------------------------------")
        print(model.names)
        print("----------------------------------------")

        print(
            "Number of classes:",
            len(model.names)
            if model.names is not None
            else "UNKNOWN"
        )

        print("========================================")

        return _model

    except Exception as e:

        print()
        print("❌ FAILED TO LOAD PALM YOLO MODEL")
        print("----------------------------------------")
        print(f"ERROR TYPE: {type(e).__name__}")
        print(f"ERROR MESSAGE: {e}")
        print("----------------------------------------")

        _model = None

        gc.collect()

        raise


# ============================================================
# NORMALIZE MODEL CLASS NAME
# ============================================================

def normalize_class_name(name):

    if name is None:
        return ""

    name = str(name).strip().lower()

    # Remove spaces / hyphens
    name = name.replace("-", "_")
    name = name.replace(" ", "_")

    return name


# ============================================================
# MAP YOLO CLASS TO PALM LINE
# ============================================================

def map_class_to_line(class_id, model_names):

    """
    Uses the actual class names stored inside best.pt.

    Supported names:
        fate
        fate_line
        head
        head_line
        heart
        heart_line
        life
        life_line

    Falls back to the original ID mapping only if the model
    class name cannot be determined.
    """

    try:

        if isinstance(model_names, dict):

            raw_name = model_names.get(
                class_id,
                ""
            )

        else:

            raw_name = model_names[class_id]

        name = normalize_class_name(raw_name)

        print(
            f"YOLO class ID {class_id} -> "
            f"model name '{name}'"
        )

        if "fate" in name:
            return "fate"

        if "heart" in name:
            return "heart"

        if "head" in name:
            return "head"

        if "life" in name:
            return "life"

    except Exception as e:

        print(
            f"⚠️ Could not map class name: {e}"
        )

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    fallback = {
        0: "fate",
        1: "head",
        2: "heart",
        3: "life",
    }

    return fallback.get(
        class_id
    )


# ============================================================
# PALM LINE ANALYSIS
# ============================================================

def analyze_palm_image(image_path):

    """
    Run YOLO palm-line detection.
    """

    import torch

    # --------------------------------------------------------
    # Configure CPU
    # --------------------------------------------------------

    try:
        torch.set_num_threads(1)
    except Exception:
        pass

    try:
        torch.set_num_interop_threads(1)
    except Exception:
        pass

    # --------------------------------------------------------
    # Validate image
    # --------------------------------------------------------

    if not os.path.isfile(image_path):

        raise FileNotFoundError(
            f"""
Palm image not found:

{image_path}
"""
        )

    print()
    print("========================================")
    print("PALM ANALYSIS")
    print("========================================")
    print(f"Image: {image_path}")

    # --------------------------------------------------------
    # Load model
    # --------------------------------------------------------

    model = get_model()

    print()
    print("🔥 MODEL CLASS NAMES:")
    print(model.names)

    # ========================================================
    # INITIALIZE PALM LINES
    # ========================================================

    palm_lines = {

        "fate": {
            "detected": False,
            "confidence": 0.0,
            "confidence_percent": 0.0,
            "length_pixels": 0.0,
            "start_point": None,
            "end_point": None,
            "angle_degrees": 0.0,
            "average_curvature_degrees": 0.0,
            "keypoint_count": 0,
        },

        "head": {
            "detected": False,
            "confidence": 0.0,
            "confidence_percent": 0.0,
            "length_pixels": 0.0,
            "start_point": None,
            "end_point": None,
            "angle_degrees": 0.0,
            "average_curvature_degrees": 0.0,
            "keypoint_count": 0,
        },

        "heart": {
            "detected": False,
            "confidence": 0.0,
            "confidence_percent": 0.0,
            "length_pixels": 0.0,
            "start_point": None,
            "end_point": None,
            "angle_degrees": 0.0,
            "average_curvature_degrees": 0.0,
            "keypoint_count": 0,
        },

        "life": {
            "detected": False,
            "confidence": 0.0,
            "confidence_percent": 0.0,
            "length_pixels": 0.0,
            "start_point": None,
            "end_point": None,
            "angle_degrees": 0.0,
            "average_curvature_degrees": 0.0,
            "keypoint_count": 0,
        },
    }

    results = None
    result = None

    # ========================================================
    # YOLO INFERENCE
    # ========================================================

    try:

        print()
        print("========== YOLO INFERENCE ==========")
        print("Running YOLO inference on CPU...")

        # ----------------------------------------------------
        # IMPORTANT CHANGES
        #
        # Palm lines are very thin.
        #
        # Previous:
        #   imgsz = 640
        #   conf = 0.05
        #
        # Now:
        #   imgsz = 1024
        #   conf = 0.001
        #
        # This allows us to inspect very weak detections.
        # ----------------------------------------------------

        print("Image size: 1024")
        print("Confidence threshold: 0.001")

        start_time = time.time()

        with torch.inference_mode():

            results = model.predict(

                source=image_path,

                imgsz=1024,

                conf=0.001,

                iou=0.5,

                device="cpu",

                half=False,

                verbose=False,

                max_det=20,

                batch=1,

                augment=False,

            )

        elapsed = time.time() - start_time

        print(
            f"YOLO inference time: {elapsed:.2f} seconds"
        )

        print("✅ YOLO inference completed.")

        # ====================================================
        # VALIDATE RESULTS
        # ====================================================

        if not results:

            raise RuntimeError(
                "YOLO returned no results."
            )

        result = results[0]

        boxes = result.boxes

        detection_count = (
            len(boxes)
            if boxes is not None
            else 0
        )

        print()
        print(
            f"🔥 NUMBER OF DETECTIONS: "
            f"{detection_count}"
        )

        # ====================================================
        # NO DETECTIONS
        # ====================================================

        if (
            boxes is None
            or len(boxes) == 0
        ):

            print()
            print(
                "⚠️ YOLO FOUND NO DETECTIONS "
                "EVEN AT CONFIDENCE 0.001"
            )

            print()
            print(
                "This indicates one of the following:"
            )

            print(
                "1. best.pt is not trained correctly "
                "for this palm image."
            )

            print(
                "2. The uploaded palm image is very "
                "different from the training images."
            )

            print(
                "3. The model is a different model "
                "than expected."
            )

            print(
                "4. The palm lines are not detectable "
                "by this YOLO model."
            )

            return {
                "palm_lines": palm_lines,
                "overall_confidence": 0.0,
            }

        # ====================================================
        # PRINT ALL RAW DETECTIONS
        # ====================================================

        print()
        print("🔥 RAW YOLO DETECTIONS")
        print("----------------------------------------")

        for i in range(len(boxes)):

            try:

                class_id = int(
                    boxes.cls[i].item()
                )

            except Exception:

                class_id = -1

            try:

                confidence = float(
                    boxes.conf[i].item()
                )

            except Exception:

                confidence = 0.0

            try:

                if isinstance(
                    model.names,
                    dict
                ):

                    model_class = model.names.get(
                        class_id,
                        "unknown"
                    )

                else:

                    model_class = model.names[
                        class_id
                    ]

            except Exception:

                model_class = "unknown"

            print(
                f"Detection {i}: "
                f"class_id={class_id}, "
                f"class={model_class}, "
                f"confidence={confidence:.6f}"
            )

        print("----------------------------------------")

        # ====================================================
        # KEYPOINTS
        # ====================================================

        keypoints = result.keypoints

        # ====================================================
        # PROCESS DETECTIONS
        # ====================================================

        for i in range(len(boxes)):

            # ------------------------------------------------
            # CLASS ID
            # ------------------------------------------------

            try:

                class_id = int(
                    boxes.cls[i].item()
                )

            except Exception as e:

                print(
                    f"⚠️ Could not read class ID: {e}"
                )

                continue

            # ------------------------------------------------
            # CONFIDENCE
            # ------------------------------------------------

            try:

                confidence = float(
                    boxes.conf[i].item()
                )

            except Exception as e:

                print(
                    f"⚠️ Could not read confidence: {e}"
                )

                continue

            # ------------------------------------------------
            # MAP CLASS
            # ------------------------------------------------

            line_name = map_class_to_line(
                class_id,
                model.names
            )

            if line_name is None:

                print(
                    f"⚠️ Unknown YOLO class: "
                    f"{class_id}"
                )

                continue

            print()
            print(
                f"🔥 PROCESSING DETECTION {i}"
            )

            print(
                f"Class ID: {class_id}"
            )

            print(
                f"Mapped line: {line_name}"
            )

            print(
                f"Confidence: {confidence:.6f}"
            )

            # ------------------------------------------------
            # Keep best detection
            # ------------------------------------------------

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

                print(
                    f"⚠️ No keypoints available "
                    f"for {line_name}"
                )

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
                    f"⚠️ Keypoint extraction "
                    f"failed for {line_name}: {e}"
                )

                continue

            if (
                points is None
                or len(points) == 0
            ):

                print(
                    f"⚠️ No keypoints found "
                    f"for {line_name}"
                )

                continue

            # =================================================
            # VALID KEYPOINTS
            # =================================================

            valid_points = []

            for point in points:

                try:

                    x = float(point[0])
                    y = float(point[1])

                except Exception:

                    continue

                if (
                    x > 0
                    and y > 0
                ):

                    valid_points.append(
                        (x, y)
                    )

            if len(valid_points) < 2:

                print(
                    f"⚠️ Less than 2 valid "
                    f"keypoints for {line_name}"
                )

                continue

            palm_lines[line_name][
                "keypoint_count"
            ] = len(valid_points)

            # =================================================
            # START / END
            # =================================================

            start_x, start_y = valid_points[0]
            end_x, end_y = valid_points[-1]

            palm_lines[line_name][
                "start_point"
            ] = {
                "x": round(start_x, 2),
                "y": round(start_y, 2),
            }

            palm_lines[line_name][
                "end_point"
            ] = {
                "x": round(end_x, 2),
                "y": round(end_y, 2),
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

                dx = x2 - x1
                dy = y2 - y1

                total_length += math.sqrt(
                    dx * dx + dy * dy
                )

            palm_lines[line_name][
                "length_pixels"
            ] = round(
                total_length,
                2
            )

            # =================================================
            # ANGLE
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
            # CURVATURE
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
                    difference = 360 - difference

                angles.append(
                    difference
                )

            if angles:

                palm_lines[line_name][
                    "average_curvature_degrees"
                ] = round(
                    sum(angles) / len(angles),
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
                sum(detected_confidences)
                /
                len(detected_confidences)
            )

        else:

            overall_confidence = 0.0

        # ====================================================
        # FINAL YOLO RESULT
        # ====================================================

        print()
        print("========================================")
        print("BEST PALM LINE DETECTIONS")
        print("========================================")

        for name, data in palm_lines.items():

            print(
                f"{name.upper():<8} -> "
                f"Detected: {data['detected']} | "
                f"Confidence: "
                f"{data['confidence_percent']:.1f}% | "
                f"Keypoints: "
                f"{data['keypoint_count']}"
            )

        print()

        print(
            f"Overall confidence -> "
            f"{overall_confidence * 100:.1f}%"
        )

        print("========================================")
        print()

        return {
            "palm_lines": palm_lines,
            "overall_confidence": round(
                overall_confidence,
                4
            ),
        }

    except Exception as e:

        print()
        print("❌ PALM YOLO INFERENCE FAILED")
        print("----------------------------------------")
        print(f"ERROR TYPE: {type(e).__name__}")
        print(f"ERROR MESSAGE: {e}")
        print("----------------------------------------")

        raise

    finally:

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

    palm_features = {

        "line_detection":
            palm_analysis["palm_lines"],

        "analysis_confidence":
            palm_analysis["overall_confidence"],

    }

    print()
    print("========================================")
    print("SENDING PALM FEATURES TO AI")
    print("========================================")

    reading = generate_palm_reading(
        profile,
        palm_features
    )

    print("✅ AI palm reading completed.")
    print()

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
        OpenRouter AI Reading
          ↓
        Final Result
    """

    if profile is None:
        profile = {}

    print()
    print(
        "========== PALM ANALYSIS STARTED =========="
    )

    # ========================================================
    # STEP 1 : YOLO
    # ========================================================

    palm_analysis = analyze_palm_image(
        image_path
    )

    # ========================================================
    # STEP 2 : AI
    # ========================================================

    try:

        reading = generate_reading(
            profile,
            palm_analysis
        )

    except Exception as e:

        print()
        print("❌ AI PALM READING FAILED")
        print("----------------------------------------")
        print(
            f"{type(e).__name__}: {e}"
        )
        print("----------------------------------------")

        reading = {
            "error": str(e)
        }

    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return {

        "success":
            True,

        "image_path":
            image_path,

        "palm_analysis":
            palm_analysis,

        "reading":
            reading,
    }

