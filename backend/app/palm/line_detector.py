import cv2
import numpy as np


def detect_palm_lines(image):
    """
    Detect candidate palm lines using OpenCV image enhancement
    and Hough Line Transform.
    """

    # Convert to grayscale
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image.copy()

    # Improve contrast
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )
    enhanced = clahe.apply(gray)

    # Remove noise
    blurred = cv2.GaussianBlur(
        enhanced,
        (5, 5),
        0
    )

    # Adaptive Threshold
    binary = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2
    )

    # Morphological cleanup
    kernel = np.ones((3, 3), np.uint8)

    cleaned = cv2.morphologyEx(
        binary,
        cv2.MORPH_OPEN,
        kernel
    )

    # Edge Detection
    edges = cv2.Canny(
        cleaned,
        50,
        150
    )

    # Detect line segments
    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=30,
        minLineLength=20,
        maxLineGap=10
    )

    candidate_lines = []

    if lines is not None:
        for line in lines:
            candidate_lines.append(line[0])

    return candidate_lines