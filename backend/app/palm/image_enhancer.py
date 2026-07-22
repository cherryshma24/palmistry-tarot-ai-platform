import cv2
import numpy as np


def enhance_palm_image(rgb_image):
    """
    Enhance palm image for line detection.
    """

    gray = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)

    # Reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Improve contrast
    enhanced = cv2.equalizeHist(blurred)

    return enhanced