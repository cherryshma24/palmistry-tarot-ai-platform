import math


def calculate_distance(point1, point2):
    return math.sqrt(
        (point1["x"] - point2["x"]) ** 2 +
        (point1["y"] - point2["y"]) ** 2
    )


def extract_palm_features(landmarks):
    wrist = landmarks[0]

    # Finger tips
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    little_tip = landmarks[20]

    # Finger MCP joints
    thumb_mcp = landmarks[2]
    index_mcp = landmarks[5]
    middle_mcp = landmarks[9]
    ring_mcp = landmarks[13]
    little_mcp = landmarks[17]

    # Basic finger lengths
    thumb_length = calculate_distance(thumb_tip, thumb_mcp)
    index_length = calculate_distance(index_tip, index_mcp)
    middle_length = calculate_distance(middle_tip, middle_mcp)
    ring_length = calculate_distance(ring_tip, ring_mcp)
    little_length = calculate_distance(little_tip, little_mcp)

    # Palm dimensions
    palm_width = calculate_distance(index_mcp, little_mcp)
    palm_height = calculate_distance(wrist, middle_mcp)
    palm_aspect_ratio = palm_height / palm_width if palm_width else 0

    # Average finger length
    avg_finger_length = (
        thumb_length +
        index_length +
        middle_length +
        ring_length +
        little_length
    ) / 5

    # Finger ratios
    index_middle_ratio = index_length / middle_length if middle_length else 0
    ring_middle_ratio = ring_length / middle_length if middle_length else 0
    little_ring_ratio = little_length / ring_length if ring_length else 0

    # Finger spread
    thumb_index_spread = calculate_distance(thumb_tip, index_tip)
    index_middle_spread = calculate_distance(index_tip, middle_tip)
    middle_ring_spread = calculate_distance(middle_tip, ring_tip)
    ring_little_spread = calculate_distance(ring_tip, little_tip)

    # Wrist to finger distances
    wrist_to_thumb = calculate_distance(wrist, thumb_tip)
    wrist_to_index = calculate_distance(wrist, index_tip)
    wrist_to_middle = calculate_distance(wrist, middle_tip)
    wrist_to_ring = calculate_distance(wrist, ring_tip)
    wrist_to_little = calculate_distance(wrist, little_tip)

    # Palm center
    palm_center_x = round((index_mcp["x"] + little_mcp["x"] + wrist["x"]) / 3, 4)
    palm_center_y = round((index_mcp["y"] + little_mcp["y"] + wrist["y"]) / 3, 4)

    # Hand orientation
    hand_orientation = (
        "Right"
        if thumb_tip["x"] < little_tip["x"]
        else "Left"
    )

    # Confidence score
    analysis_confidence = 0.95 if palm_width > 0 and palm_height > 0 else 0.0

    features = {
        # Basic finger lengths
        "thumb_length": round(thumb_length, 4),
        "index_length": round(index_length, 4),
        "middle_length": round(middle_length, 4),
        "ring_length": round(ring_length, 4),
        "little_length": round(little_length, 4),

        # Palm geometry
        "palm_width": round(palm_width, 4),
        "palm_height": round(palm_height, 4),
        "palm_aspect_ratio": round(palm_aspect_ratio, 4),
        "average_finger_length": round(avg_finger_length, 4),

        # Finger ratios
        "index_middle_ratio": round(index_middle_ratio, 4),
        "ring_middle_ratio": round(ring_middle_ratio, 4),
        "little_ring_ratio": round(little_ring_ratio, 4),

        # Finger spread
        "thumb_index_spread": round(thumb_index_spread, 4),
        "index_middle_spread": round(index_middle_spread, 4),
        "middle_ring_spread": round(middle_ring_spread, 4),
        "ring_little_spread": round(ring_little_spread, 4),

        # Wrist distances
        "wrist_to_thumb": round(wrist_to_thumb, 4),
        "wrist_to_index": round(wrist_to_index, 4),
        "wrist_to_middle": round(wrist_to_middle, 4),
        "wrist_to_ring": round(wrist_to_ring, 4),
        "wrist_to_little": round(wrist_to_little, 4),

        # Palm center
        "palm_center": {
            "x": palm_center_x,
            "y": palm_center_y
        },

        # Orientation and confidence
        "hand_orientation": hand_orientation,
        "analysis_confidence": round(analysis_confidence, 2)
    }

    return features