import os
import math
import gc

from app.services.ai_manager import generate_palm_reading


# ============================================================
# RENDER / CPU OPTIMIZATION
# ============================================================

# Keep PyTorch from creating too many CPU threads.
# This is important on small Render instances.
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")


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
# GLOBAL MODEL
# ============================================================

# YOLO is loaded only when palm analysis is requested.
#
# IMPORTANT:
# Do NOT load YOLO during FastAPI startup.
# Do NOT reload YOLO for every request.
#
# Keeping one model instance greatly reduces memory usage
# and avoids repeated PyTorch initialization.
_model = None


# ============================================================
# GET YOLO MODEL
# ============================================================

def get_model():
    """
    Load the YOLO palm model once.

    Optimized for:
        - Render free/low-resource CPU
        - FastAPI
        - CPU-only inference
        - Low memory usage

    The model is NOT loaded during application startup.
    """

    global _model

    # --------------------------------------------------------
    # Return existing model
    # --------------------------------------------------------

    if _model is not None:
        return _model

    # --------------------------------------------------------
    # Verify model exists
    # --------------------------------------------------------

    if not os.path.isfile(MODEL_PATH):
        raise FileNotFoundError(
            f"Palm YOLO model not found:\n"
            f"{MODEL_PATH}\n\n"
            "Make sure best.pt exists at:\n"
            "backend/models/palm_pose/best.pt"
        )

    print()
    print("========================================")
    print("LOADING PALM YOLO MODEL")
    print("========================================")
    print(f"Model path: {MODEL_PATH}")

    # --------------------------------------------------------
    # Import PyTorch only when needed
    # --------------------------------------------------------

    import torch

    # Limit PyTorch CPU threads.
    # This prevents excessive CPU/memory usage on Render.
    try:
        torch.set_num_threads(1)
    except Exception:
        pass

    try:
        torch.set_num_interop_threads(1)
    except Exception:
        pass

    # --------------------------------------------------------
    # Lazy import Ultralytics
    # --------------------------------------------------------

    from ultralytics import YOLO

    try:

        # ----------------------------------------------------
        # Load model
        # ----------------------------------------------------

        model = YOLO(MODEL_PATH)

        # ----------------------------------------------------
        # CPU-only mode
        # ----------------------------------------------------

        try:
            model.to("cpu")
        except Exception:
            pass

        # ----------------------------------------------------
        # Evaluation mode
        # ----------------------------------------------------

        try:
            model.model.eval()
        except Exception:
            pass

        # ----------------------------------------------------
        # Store globally
        # ----------------------------------------------------

        _model = model

        print("✅ Palm YOLO model loaded successfully.")
        print("✅ Device: CPU")
        print("========================================")
        print()

        return _model

    except Exception as e:

        print()
        print("❌ FAILED TO LOAD PALM YOLO MODEL")
        print("----------------------------------------")
        print(str(e))
        print("----------------------------------------")

        _model = None

        gc.collect()

        raise


# ============================================================
# PALM LINE ANALYSIS
# ============================================================

def analyze_palm_image(image_path):
    """
    Run YOLO palm-line detection.

    Extracts:

        - confidence
        - keypoints
        - line length
        - start point
        - end point
        - angle
        - average curvature

    Render optimizations:

        - CPU-only
        - 320px inference size
        - inference_mode()
        - one YOLO model instance
        - one PyTorch CPU thread
        - limited detections
        - explicit garbage collection
    """

    import torch

    # --------------------------------------------------------
    # Configure PyTorch CPU
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
            f"Palm image not found:\n{image_path}"
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

        print("Running YOLO inference on CPU...")
        print("Image size: 256")
        print("Confidence threshold: 0.05")

        # ----------------------------------------------------
        # Disable gradients completely
        # ----------------------------------------------------
        import time

        start_time = time.time() 
        with torch.inference_mode():

            results = model.predict(

                source=image_path,

                # ------------------------------------------------
                # LOW-MEMORY IMAGE SIZE
                # ------------------------------------------------
                #
                # 320 is enough for the palm-line task and
                # reduces CPU/RAM usage compared with 640.
                #
                imgsz=256,

                # ------------------------------------------------
                # CONFIDENCE
                # ------------------------------------------------

                conf=0.05,

                # ------------------------------------------------
                # CPU ONLY
                # ------------------------------------------------

                device="cpu",

                # ------------------------------------------------
                # DO NOT USE HALF PRECISION ON CPU
                # ------------------------------------------------

                half=False,

                # ------------------------------------------------
                # NO VERBOSE OUTPUT
                # ------------------------------------------------

                verbose=False,

                # ------------------------------------------------
                # LIMIT DETECTIONS
                # ------------------------------------------------

                max_det=10,

                # ------------------------------------------------
                # Single image
                # ------------------------------------------------

                batch=1,

                # ------------------------------------------------
                # Avoid unnecessary augmentation
                # ------------------------------------------------

                augment=False
            )
            elapsed = time.time() - start_time
            print(f"YOLO inference time: {elapsed:.2f} seconds")

        print("✅ YOLO inference completed.")

        # ====================================================
        # VALIDATE RESULT
        # ====================================================

        if not results:

            raise RuntimeError(
                "YOLO returned no results."
            )

        result = results[0]

        # ====================================================
        # CHECK BOXES
        # ====================================================

        boxes = result.boxes

        if (
            boxes is None
            or len(boxes) == 0
        ):

            print("⚠️ No palm lines detected.")

            return {
                "palm_lines": palm_lines,
                "overall_confidence": 0.0
            }

        # ====================================================
        # KEYPOINTS
        # ====================================================

        keypoints = result.keypoints

        # ====================================================
        # PROCESS DETECTIONS
        # ====================================================

        for i in range(len(boxes)):

            # ------------------------------------------------
            # CLASS
            # ------------------------------------------------

            try:

                class_id = int(
                    boxes.cls[i].item()
                )

            except Exception:

                continue

            if class_id not in class_names:
                continue

            line_name = class_names[class_id]

            # ------------------------------------------------
            # CONFIDENCE
            # ------------------------------------------------

            try:

                confidence = float(
                    boxes.conf[i].item()
                )

            except Exception:

                continue

            # ------------------------------------------------
            # KEEP BEST DETECTION
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
                    f"⚠️ Keypoint extraction failed "
                    f"for {line_name}: {e}"
                )

                continue

            if (
                points is None
                or len(points) == 0
            ):
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

                # Ignore invalid coordinates.
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
        # PRINT RESULTS
        # ====================================================

        print()
        print("========================================")
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

        print("========================================")
        print()

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

    except Exception as e:

        # ----------------------------------------------------
        # IMPORTANT ERROR LOGGING
        # ----------------------------------------------------

        print()
        print("❌ PALM YOLO INFERENCE FAILED")
        print("----------------------------------------")
        print(f"{type(e).__name__}: {e}")
        print("----------------------------------------")

        raise

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

        # ----------------------------------------------------
        # Force Python garbage collection.
        # ----------------------------------------------------

        try:
            gc.collect()
        except Exception:
            pass

        # ----------------------------------------------------
        # CUDA cleanup only if CUDA exists.
        # Render deployment is CPU-only.
        # ----------------------------------------------------

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
        Feature Extraction
          ↓
        OpenRouter AI Reading
          ↓
        Final Result
    """

    if profile is None:
        profile = {}

    print()
    print("========== PALM ANALYSIS STARTED ==========")

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

        print()
        print("❌ AI PALM READING FAILED")
        print("----------------------------------------")
        print(f"{type(e).__name__}: {e}")
        print("----------------------------------------")

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