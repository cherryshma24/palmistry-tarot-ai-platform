def generate_palm_reading(features):
    """
    Generate a dynamic palm reading using extracted palm features.
    """

    reading = {}

    # -------------------------
    # Personality
    # -------------------------

    if (
        features["average_finger_length"] > 0.30
        and features["palm_aspect_ratio"] > 1.15
    ):
        reading["personality"] = (
            "You are thoughtful, analytical, and enjoy learning new ideas. "
            "You usually think before making decisions."
        )

    elif features["palm_width"] > 0.38:
        reading["personality"] = (
            "You are practical, confident, and enjoy taking responsibility."
        )

    else:
        reading["personality"] = (
            "You are calm, balanced, and prefer stability in life."
        )

    # -------------------------
    # Career
    # -------------------------

    if (
        features["index_middle_ratio"] > 0.88
        and features["thumb_length"] > 0.24
    ):
        reading["career"] = (
            "Leadership, technology, engineering, and management are suitable career paths."
        )

    elif features["ring_middle_ratio"] > 0.90:
        reading["career"] = (
            "Creative fields, media, design, and entrepreneurship may suit you."
        )

    else:
        reading["career"] = (
            "You perform well in structured and collaborative environments."
        )

    # -------------------------
    # Relationships
    # -------------------------

    if features["thumb_index_spread"] > 0.40:
        reading["relationships"] = (
            "You are open-minded, trustworthy, and value honest communication."
        )

    else:
        reading["relationships"] = (
            "You build relationships slowly but create long-lasting bonds."
        )

    # -------------------------
    # Finance
    # -------------------------

    if features["thumb_length"] > 0.25:
        reading["finance"] = (
            "You tend to manage money carefully and make practical financial decisions."
        )

    else:
        reading["finance"] = (
            "Financial growth improves through careful planning and disciplined saving."
        )

    # -------------------------
    # Health & Wellness
    # -------------------------

    if features["palm_aspect_ratio"] > 1.15:
        reading["health_wellness"] = (
            "Maintaining work-life balance, regular exercise, and proper rest will benefit you."
        )

    else:
        reading["health_wellness"] = (
            "A balanced lifestyle and stress management will support your overall well-being."
        )

    # -------------------------
    # Personal Growth
    # -------------------------

    reading["personal_growth"] = (
        "Continue learning new skills, embrace challenges, and maintain consistency toward your goals."
    )

    # -------------------------
    # Life Opportunities
    # -------------------------

    if features["average_finger_length"] > 0.30:
        reading["life_opportunities"] = (
            "Future opportunities are likely to come through education, innovation, and leadership."
        )

    else:
        reading["life_opportunities"] = (
            "Steady progress and patience will open new opportunities over time."
        )

    # -------------------------
    # Strengths
    # -------------------------

    strengths = []

    if features["thumb_length"] > 0.24:
        strengths.append("Strong determination")

    if features["index_middle_ratio"] > 0.85:
        strengths.append("Leadership ability")

    if features["average_finger_length"] > 0.30:
        strengths.append("Analytical thinking")

    if features["thumb_index_spread"] > 0.40:
        strengths.append("Excellent communication")

    if features["palm_aspect_ratio"] > 1.15:
        strengths.append("Problem-solving skills")

    if not strengths:
        strengths.append("Balanced personality")

    reading["strengths"] = strengths

    # -------------------------
    # Overall Summary
    # -------------------------

    reading["overall_summary"] = (
        "Your palm indicates a balanced personality with good potential for personal growth, "
        "career development, and meaningful relationships."
    )

    # -------------------------
    # Confidence
    # -------------------------

    reading["confidence"] = features["analysis_confidence"]

    return reading