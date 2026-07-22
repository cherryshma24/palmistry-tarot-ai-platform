import cv2
import numpy as np


def preprocess_image(image_bytes: bytes):
    """
    Convert uploaded image bytes into an OpenCV image and preprocess it.
    """

    # Convert bytes to numpy array
    np_array = np.frombuffer(image_bytes, np.uint8)

    # Decode image
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Invalid image.")

    # Resize image
    image = cv2.resize(image, (640, 480))

    # Convert BGR to RGB (required for MediaPipe)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image, rgb_image