import json

from app.services.gemini_service import generate_text


def generate_palm_reading(profile, palm_features):
    """
    Generate Palm Reading using AI.
    Falls back to dynamic rule-based reading if AI fails.
    """

    prompt = f"""
You are an expert Palmistry AI.

User Profile:
{json.dumps(profile, indent=2)}

Palm Features:
{json.dumps(palm_features, indent=2)}

Analyze the palm features and generate a personalized reading.

Return ONLY valid JSON in this exact format:

{{
    "life_line":"...",
    "heart_line":"...",
    "head_line":"...",
    "fate_line":"...",
    "love_prediction":"...",
    "career_prediction":"...",
    "finance_prediction":"...",
    "health_prediction":"...",
    "overall_summary":"...",
    "fortune_score": <integer between 70 and 98>
}}

Rules:
- Return ONLY JSON.
- Do NOT use markdown.
- Do NOT include explanations.
- fortune_score MUST be calculated from the detected palm features.
- Do NOT always return the same fortune_score.
"""

    try:

        response = generate_text(prompt)

        if response:

            response = response.strip()

            if response.startswith("```"):
                response = (
                    response.replace("```json", "")
                    .replace("```", "")
                    .strip()
                )

            return json.loads(response)

    except Exception as e:
        print("AI Error:", e)

    # ==========================================================
    # Dynamic Fallback
    # ==========================================================

    palm_shape = palm_features.get("palm_shape", "Unknown")
    line_info = palm_features.get("line_detection", {})
    line_quality = line_info.get("line_quality", "Moderate")

    if isinstance(palm_shape, dict):
        palm_shape_name = (
            palm_shape.get("shape")
            or palm_shape.get("name")
            or palm_shape.get("type")
            or "Unknown"
        )
    else:
        palm_shape_name = str(palm_shape)

    confidence = palm_features.get("analysis_confidence", 0.90)

    life = palm_features.get("life_line_length", 0.18)
    heart = palm_features.get("heart_line_length", 0.18)
    head = palm_features.get("head_line_length", 0.18)
    fate = palm_features.get("fate_line_length", 0.16)

    score = (
        confidence * 0.40
        + life * 0.15
        + heart * 0.15
        + head * 0.15
        + fate * 0.15
    ) * 100

    fortune_score = max(70, min(98, round(score)))

    return {

        "life_line":
        f"The detected life line is of {line_quality.lower()} quality, indicating resilience, vitality, and the ability to overcome challenges.",

        "heart_line":
        "Your heart line suggests emotional balance, compassion, and meaningful relationships built on trust.",

        "head_line":
        "Your head line reflects logical thinking, creativity, and strong decision-making abilities.",

        "fate_line":
        f"Your {palm_shape_name.lower()} palm shape indicates determination, persistence, and steady career growth.",

        "love_prediction":
        "Your palm suggests healthy communication, emotional maturity, and supportive relationships.",

        "career_prediction":
        "Your palm features indicate leadership qualities, practical thinking, and excellent problem-solving skills.",

        "finance_prediction":
        "Your palm analysis suggests disciplined financial habits with opportunities for long-term stability and growth.",

        "health_prediction":
        "Maintain a balanced lifestyle, regular exercise, and proper rest to continue supporting your overall well-being.",

        "overall_summary":
        (
            f"The AI analysis detected a {palm_shape_name} palm with "
            f"{line_quality.lower()} line quality. "
            "The extracted palm characteristics suggest a balanced personality, "
            "good analytical ability, emotional stability, and promising career potential. "
            "This report combines computer vision, palm feature extraction, and AI-powered palmistry interpretation."
        ),

        "fortune_score": fortune_score
    }


def generate_tarot_reading(cards):
    """
    Generate Tarot Reading using AI.
    Falls back to dataset-based interpretation.
    """

    prompt = f"""
You are an expert Tarot Reader.

Cards:
{json.dumps(cards, indent=2)}

Generate a detailed, positive, and encouraging tarot interpretation.
"""

    try:

        response = generate_text(prompt)

        if response:
            return response.strip()

    except Exception as e:
        print("AI Error:", e)

    card_names = ", ".join(card["name"] for card in cards)

    return (
        f"This reading is based on the selected card(s): {card_names}. "
        "The cards suggest new opportunities, personal growth, thoughtful decisions, "
        "and positive transformation. Treat this reading as guidance and inspiration "
        "for your journey."
    )