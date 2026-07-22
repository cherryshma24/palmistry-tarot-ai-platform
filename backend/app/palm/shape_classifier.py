import math


def distance(p1, p2):
    return math.sqrt(
        (p1["x"] - p2["x"]) ** 2 +
        (p1["y"] - p2["y"]) ** 2
    )


def classify_palm_shape(landmarks):
    """
    Classify palm shape using multiple geometric features.
    """

    wrist = landmarks[0]

    index_base = landmarks[5]
    middle_base = landmarks[9]
    ring_base = landmarks[13]
    little_base = landmarks[17]

    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    little_tip = landmarks[20]

    thumb_tip = landmarks[4]

    # Palm dimensions
    palm_length = distance(wrist, middle_base)
    palm_width = distance(index_base, little_base)

    ratio = palm_length / palm_width

    # Finger lengths
    index_length = distance(index_base, index_tip)
    middle_length = distance(middle_base, middle_tip)
    ring_length = distance(ring_base, ring_tip)
    little_length = distance(little_base, little_tip)

    average_finger_length = (
        index_length +
        middle_length +
        ring_length +
        little_length
    ) / 4

    # Finger spread
    finger_spread = distance(index_tip, little_tip)

    # Thumb spread
    thumb_spread = distance(thumb_tip, index_tip)

    # Shape classification
    if ratio < 0.90:
        shape = "Earth"

    elif ratio < 1.10:
        shape = "Fire"

    elif ratio < 1.25:
        shape = "Air"

    else:
        shape = "Water"

    # Simple confidence score
    confidence = 0.90

    if average_finger_length > 0.40:
        confidence += 0.03

    if finger_spread > 0.30:
        confidence += 0.02

    confidence = min(confidence, 0.99)

    return {
        "shape": shape,

        "palm_length": round(palm_length, 4),

        "palm_width": round(palm_width, 4),

        "ratio": round(ratio, 4),

        "average_finger_length": round(
            average_finger_length,
            4
        ),

        "finger_spread": round(
            finger_spread,
            4
        ),

        "thumb_spread": round(
            thumb_spread,
            4
        ),

        "confidence": round(
            confidence,
            2
        )
    }