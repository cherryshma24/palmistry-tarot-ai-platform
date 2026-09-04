import cv2
import numpy as np


def detect_palm_lines(image):
    """
    Detect candidate palm-line structures using OpenCV.

    Returns:
        candidate_lines: Hough line segments
        processed: enhanced binary/edge image for debugging
    """

    # Convert to grayscale
    if len(image.shape) == 3:
        # Use RGB2GRAY if image came from PIL / RGB
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image.copy()

    # Normalize image size
    gray = cv2.normalize(
        gray,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    # Improve local contrast
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(gray)

    # Smooth small noise
    blurred = cv2.GaussianBlur(
        enhanced,
        (5, 5),
        0
    )

    # Adaptive threshold
    binary = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        21,
        4
    )

    # Morphological cleanup
    kernel = np.ones((3, 3), np.uint8)

    cleaned = cv2.morphologyEx(
        binary,
        cv2.MORPH_OPEN,
        kernel,
        iterations=1
    )

    # Close small gaps in palm creases
    cleaned = cv2.morphologyEx(
        cleaned,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2
    )

    # Edge detection
    edges = cv2.Canny(
        cleaned,
        30,
        100
    )

    # Detect candidate straight segments
    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=20,
        minLineLength=15,
        maxLineGap=20
    )

    candidate_lines = []

    if lines is not None:

        for line in lines:
            x1, y1, x2, y2 = line[0]

            length = np.sqrt(
                (x2 - x1) ** 2 +
                (y2 - y1) ** 2
            )

            # Ignore very small segments
            if length >= 15:
                candidate_lines.append({
                    "x1": int(x1),
                    "y1": int(y1),
                    "x2": int(x2),
                    "y2": int(y2),
                    "length": float(length)
                })

    return candidate_lines, edges