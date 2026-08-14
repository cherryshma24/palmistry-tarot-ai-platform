import math


def calculate_distance(point1, point2):
    return math.sqrt(
        (point1["x"] - point2["x"]) ** 2 +
        (point1["y"] - point2["y"]) ** 2
    )


def extract_palm_features(landmarks):

    if landmarks is None or len(landmarks) < 21:
        return {
            "analysis_confidence": 0.0,
            "message": "Insufficient hand landmarks detected."
        }


    wrist = landmarks[0]

    # Finger tips
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    little_tip = landmarks[20]


    # MCP joints
    thumb_mcp = landmarks[2]
    index_mcp = landmarks[5]
    middle_mcp = landmarks[9]
    ring_mcp = landmarks[13]
    little_mcp = landmarks[17]


    # Finger lengths
    thumb_length = calculate_distance(
        thumb_tip, thumb_mcp
    )

    index_length = calculate_distance(
        index_tip, index_mcp
    )

    middle_length = calculate_distance(
        middle_tip, middle_mcp
    )

    ring_length = calculate_distance(
        ring_tip, ring_mcp
    )

    little_length = calculate_distance(
        little_tip, little_mcp
    )


    # Palm geometry
    palm_width = calculate_distance(
        index_mcp,
        little_mcp
    )

    palm_height = calculate_distance(
        wrist,
        middle_mcp
    )

    palm_aspect_ratio = (
        palm_height / palm_width
        if palm_width else 0
    )


    average_finger_length = (
        thumb_length +
        index_length +
        middle_length +
        ring_length +
        little_length
    ) / 5


    # Ratios
    index_middle_ratio = (
        index_length / middle_length
        if middle_length else 0
    )

    ring_middle_ratio = (
        ring_length / middle_length
        if middle_length else 0
    )

    little_ring_ratio = (
        little_length / ring_length
        if ring_length else 0
    )


    # Finger spread
    thumb_index_spread = calculate_distance(
        thumb_tip,
        index_tip
    )

    index_middle_spread = calculate_distance(
        index_tip,
        middle_tip
    )

    middle_ring_spread = calculate_distance(
        middle_tip,
        ring_tip
    )

    ring_little_spread = calculate_distance(
        ring_tip,
        little_tip
    )


    # Palm center
    palm_center = {
        "x": round(
            (
                index_mcp["x"] +
                little_mcp["x"] +
                wrist["x"]
            ) / 3,
            4
        ),

        "y": round(
            (
                index_mcp["y"] +
                little_mcp["y"] +
                wrist["y"]
            ) / 3,
            4
        )
    }


    hand_orientation = (
        "Right"
        if thumb_tip["x"] < little_tip["x"]
        else "Left"
    )


    return {

        "thumb_length": round(
            thumb_length, 4
        ),

        "index_length": round(
            index_length, 4
        ),

        "middle_length": round(
            middle_length, 4
        ),

        "ring_length": round(
            ring_length, 4
        ),

        "little_length": round(
            little_length, 4
        ),


        "palm_width": round(
            palm_width, 4
        ),

        "palm_height": round(
            palm_height, 4
        ),

        "palm_aspect_ratio": round(
            palm_aspect_ratio, 4
        ),


        "average_finger_length": round(
            average_finger_length, 4
        ),


        "index_middle_ratio": round(
            index_middle_ratio, 4
        ),

        "ring_middle_ratio": round(
            ring_middle_ratio, 4
        ),

        "little_ring_ratio": round(
            little_ring_ratio, 4
        ),


        "thumb_index_spread": round(
            thumb_index_spread, 4
        ),

        "index_middle_spread": round(
            index_middle_spread, 4
        ),

        "middle_ring_spread": round(
            middle_ring_spread, 4
        ),

        "ring_little_spread": round(
            ring_little_spread, 4
        ),


        "palm_center": palm_center,


        "hand_orientation": hand_orientation,


        "analysis_confidence": 0.95

    }