import json

from app.services.openrouter_service import ask_ai


# ============================================================
# HELPER — CLEAN AI JSON RESPONSE
# ============================================================

def _parse_ai_json(response):
    """
    Convert the AI response into a Python dictionary.

    Handles normal JSON and JSON wrapped in markdown fences.
    """

    if not response:
        return None

    response = response.strip()

    if response.startswith("```json"):
        response = response[7:]

    elif response.startswith("```"):
        response = response[3:]

    if response.endswith("```"):
        response = response[:-3]

    response = response.strip()

    return json.loads(response)


# ============================================================
# HELPER — NORMALIZE AI SCORES
# ============================================================

def _normalize_score(value, default=0):
    """
    Convert AI-generated score into a clean number from 0 to 100.
    Handles values such as:
        78
        "78"
        "78%"
        7.5
    """

    try:

        if value is None:
            return default

        if isinstance(value, str):
            value = value.strip().replace("%", "")

        score = float(value)

        score = max(0, min(100, score))

        if score.is_integer():
            return int(score)

        return round(score, 1)

    except (ValueError, TypeError):
        return default


    # ============================================================
# HELPER — NORMALIZE PALM AI RESULT
# ============================================================

def _normalize_palm_reading(reading, palm_features):
    """
    Clean and validate AI-generated palm reading.

    Computer-vision measurements are always taken from
    the actual YOLO output.
    """

    if not isinstance(reading, dict):
        return None

    line_data = palm_features.get(
        "line_detection",
        {}
    )

    if not isinstance(line_data, dict):
        line_data = {}

    palm_analysis = reading.get(
        "palm_analysis",
        {}
    )

    if not isinstance(palm_analysis, dict):
        palm_analysis = {}

    # --------------------------------------------------------
    # FORCE ACTUAL YOLO MEASUREMENTS
    # --------------------------------------------------------

    for line_name in [
        "life",
        "heart",
        "head",
        "fate"
    ]:

        actual = line_data.get(
            line_name,
            {}
        )

        if not isinstance(actual, dict):
            actual = {}

        ai_line = palm_analysis.get(
            f"{line_name}_line",
            {}
        )

        if not isinstance(ai_line, dict):
            ai_line = {}

        ai_line["confidence_percent"] = actual.get(
            "confidence_percent",
            0
        )

        ai_line["length_pixels"] = actual.get(
            "length_pixels",
            0
        )

        ai_line["angle_degrees"] = actual.get(
            "angle_degrees",
            0
        )

        ai_line["curvature_degrees"] = actual.get(
            "average_curvature_degrees",
            0
        )

        palm_analysis[
            f"{line_name}_line"
        ] = ai_line

    reading["palm_analysis"] = palm_analysis

    # --------------------------------------------------------
    # OVERALL CV CONFIDENCE
    # --------------------------------------------------------

    actual_confidence = palm_features.get(
        "analysis_confidence",
        0
    )

    if isinstance(actual_confidence, (int, float)):

        if actual_confidence <= 1:
            actual_confidence *= 100

    reading["confidence"] = round(
        max(
            0,
            min(
                100,
                float(actual_confidence)
            )
        ),
        1
    )

    # --------------------------------------------------------
    # CAREER SCORE
    # --------------------------------------------------------

    career = reading.get(
        "career",
        {}
    )

    if not isinstance(career, dict):
        career = {}

    career["career_score"] = _normalize_score(
        career.get("career_score"),
        default=reading["confidence"]
    )

    reading["career"] = career

    # --------------------------------------------------------
    # FORTUNE SCORE
    # --------------------------------------------------------

    reading["fortune_score"] = _normalize_score(
        reading.get("fortune_score"),
        default=reading["confidence"]
    )

    # --------------------------------------------------------
    # DISCLAIMER
    # --------------------------------------------------------

    reading["disclaimer"] = (
        "Palmistry interpretations are for entertainment "
        "and self-reflection."
    )

    return reading


# ============================================================
# PALM READING
# ============================================================

def generate_palm_reading(profile, palm_features):
    """
    Generate AI-powered Palm Reading.

    Uses the actual computer-vision palm-line features
    extracted by the YOLO palm-line model.

    Falls back to a rule-based reading if AI fails.
    """

    analysis_payload = {
        "profile": profile,
        "palm_features": palm_features,
        "system": {
            "platform": "Palmistry & Tarot Intelligence Platform",
            "cv_engine": "YOLOv8 Pose Palm Line Detection",
            "ai_engine": "OpenRouter LLM"
        }
    }

    prompt = f"""
You are the AI Palmistry Interpretation Engine of a
Palmistry & Tarot Intelligence Platform.

Your job is to interpret palm-line features detected by
a computer-vision model.

IMPORTANT RULES:

1. Use ONLY the supplied palm_features.
2. Do NOT invent measurements.
3. Do NOT change the supplied confidence percentages.
4. The confidence percentage represents computer-vision
   detection confidence, NOT the certainty of palmistry.
5. If a line has low detection confidence, clearly mention
   that interpretation is uncertain.
6. Do NOT make medical, legal, financial or guaranteed
   future predictions.
7. Palmistry is for entertainment and self-reflection.
8. Use a positive, professional and natural tone.
9. Return ONLY valid JSON.
10. Do NOT return markdown.
11. Do NOT add explanations outside the JSON.

VERY IMPORTANT:

The actual detected line confidence values must be preserved.

For example:

Heart line confidence = 81.1%
Life line confidence = 72.3%
Head line confidence = 61.2%
Fate line confidence = 8.7%

Do not replace these values with invented confidence scores.

INPUT DATA:

{json.dumps(analysis_payload, indent=2)}

Return JSON exactly in this structure:

{{
    "personality": {{
        "traits": [],
        "strengths": [],
        "growth_areas": []
    }},

    "palm_analysis": {{
        "life_line": {{
            "confidence_percent": 0,
            "length_pixels": 0,
            "angle_degrees": 0,
            "curvature_degrees": 0,
            "interpretation": "",
            "key_observations": []
        }},

        "heart_line": {{
            "confidence_percent": 0,
            "length_pixels": 0,
            "angle_degrees": 0,
            "curvature_degrees": 0,
            "interpretation": "",
            "key_observations": []
        }},

        "head_line": {{
            "confidence_percent": 0,
            "length_pixels": 0,
            "angle_degrees": 0,
            "curvature_degrees": 0,
            "interpretation": "",
            "key_observations": []
        }},

        "fate_line": {{
            "confidence_percent": 0,
            "length_pixels": 0,
            "angle_degrees": 0,
            "curvature_degrees": 0,
            "interpretation": "",
            "key_observations": []
        }}
    }},

    "career": {{
        "prediction": "",
        "suitable_roles": [],
        "career_score": 0
    }},

    "relationships": {{
        "prediction": "",
        "compatibility": ""
    }},

    "finance": {{
        "prediction": "",
        "money_management": ""
    }},

    "health": {{
        "prediction": "",
        "wellness_tip": ""
    }},

    "recommendations": [],

    "overall_summary": "",

    "confidence": 0,

    "fortune_score": 0,

    "disclaimer": "Palmistry interpretations are for entertainment and self-reflection."
}}

SCORING RULES:

- confidence should represent the overall computer-vision
  detection quality and should be calculated from the supplied
  line confidence values.
- Do NOT artificially make confidence 80-99.
- fortune_score is an entertainment/self-reflection score,
  not a scientific prediction.
- Do not invent confidence values for individual lines.
"""

    # ========================================================
    # CALL OPENROUTER
    # ========================================================

    try:
        response = ask_ai(prompt)

        if response:
            parsed = _parse_ai_json(response)

            if parsed:
                normalized = _normalize_palm_reading(
                    parsed,
                    palm_features
                )

                if normalized:
                    return normalized

    except Exception as e:
        print("AI Palm Reading Error:", e)

    # ========================================================
    # FALLBACK READING
    # ========================================================

    print("Using rule-based palm reading fallback.")

    return _generate_palm_fallback(palm_features)


# ============================================================
# PALM FALLBACK
# ============================================================

def _generate_palm_fallback(palm_features):
    """
    Generate a safe fallback reading using actual
    detected palm-line information.
    """

    def get_line(name):

        value = palm_features.get(name, {})

        if isinstance(value, dict):
            return value

        return {}

    life = get_line("life")
    heart = get_line("heart")
    head = get_line("head")
    fate = get_line("fate")

    # --------------------------------------------------------
    # Some older versions of the project may use these names.
    # Support them as a compatibility fallback.
    # --------------------------------------------------------

    if not life:
        life = palm_features.get("life_line", {})

    if not heart:
        heart = palm_features.get("heart_line", {})

    if not head:
        head = palm_features.get("head_line", {})

    if not fate:
        fate = palm_features.get("fate_line", {})

    life_conf = float(life.get("confidence_percent", 0))
    heart_conf = float(heart.get("confidence_percent", 0))
    head_conf = float(head.get("confidence_percent", 0))
    fate_conf = float(fate.get("confidence_percent", 0))

    # Overall CV confidence
    confidence_score = round(
        (life_conf + heart_conf + head_conf + fate_conf) / 4
    )

    # Keep within sensible range
    confidence_score = max(
        0,
        min(100, confidence_score)
    )

    # Entertainment score
    fortune_score = round(
        (
            life_conf * 0.30
            + heart_conf * 0.30
            + head_conf * 0.25
            + fate_conf * 0.15
        )
    )

    fortune_score = max(
        0,
        min(100, fortune_score)
    )

    return {

        "personality": {

            "traits": [
                "Emotionally balanced",
                "Practical",
                "Observant"
            ],

            "strengths": [
                "Analytical thinking",
                "Emotional awareness",
                "Persistence"
            ],

            "growth_areas": [
                "Trust your decisions",
                "Maintain emotional balance",
                "Develop long-term clarity"
            ]
        },

        "palm_analysis": {

            "life_line": {

                "confidence_percent": life_conf,

                "length_pixels":
                    life.get("length_pixels", 0),

                "angle_degrees":
                    life.get("angle_degrees", 0),

                "curvature_degrees":
                    life.get("average_curvature_degrees", 0),

                "interpretation":
                    "The detected life line suggests energy, resilience and persistence. This is a traditional palmistry interpretation for entertainment and self-reflection.",

                "key_observations": [
                    "Life line detected",
                    f"Detection confidence: {life_conf}%"
                ]
            },

            "heart_line": {

                "confidence_percent": heart_conf,

                "length_pixels":
                    heart.get("length_pixels", 0),

                "angle_degrees":
                    heart.get("angle_degrees", 0),

                "curvature_degrees":
                    heart.get("average_curvature_degrees", 0),

                "interpretation":
                    "The detected heart line suggests emotional awareness, warmth and a balanced approach to relationships.",

                "key_observations": [
                    "Heart line detected",
                    f"Detection confidence: {heart_conf}%"
                ]
            },

            "head_line": {

                "confidence_percent": head_conf,

                "length_pixels":
                    head.get("length_pixels", 0),

                "angle_degrees":
                    head.get("angle_degrees", 0),

                "curvature_degrees":
                    head.get("average_curvature_degrees", 0),

                "interpretation":
                    "The detected head line is traditionally associated with practical thinking, focus and analytical ability.",

                "key_observations": [
                    "Head line detected",
                    f"Detection confidence: {head_conf}%"
                ]
            },

            "fate_line": {

                "confidence_percent": fate_conf,

                "length_pixels":
                    fate.get("length_pixels", 0),

                "angle_degrees":
                    fate.get("angle_degrees", 0),

                "curvature_degrees":
                    fate.get("average_curvature_degrees", 0),

                "interpretation":
                    (
                        "The fate line detection has low confidence, "
                        "so its interpretation should be treated cautiously."
                    ),

                "key_observations": [
                    "Fate line detected",
                    f"Detection confidence: {fate_conf}%"
                ]
            }
        },

        "career": {

            "prediction":
                "The detected palm features can be interpreted as suggesting persistence, practical thinking and adaptability.",

            "suitable_roles": [
                "Software Engineer",
                "AI Engineer",
                "Data Analyst",
                "Research Engineer"
            ],

            "career_score":
                fortune_score
        },

        "relationships": {

            "prediction":
                "The heart-line features are traditionally associated with emotional awareness and meaningful connections.",

            "compatibility":
                "Positive communication, honesty and mutual respect can support healthy relationships."
        },

        "finance": {

            "prediction":
                "Financial outcomes depend on real-world decisions and circumstances. The palm reading is only for entertainment.",

            "money_management":
                "Consider disciplined planning and thoughtful spending."
        },

        "health": {

            "prediction":
                "Palm lines cannot reliably determine health conditions.",

            "wellness_tip":
                "Maintain healthy habits and consult qualified professionals for health concerns."
        },

        "recommendations": [

            "Continue developing your skills.",
            "Maintain a healthy balance between work and personal life.",
            "Use self-reflection to clarify long-term goals."
        ],

        "overall_summary":
            (
                "Computer vision detected the major palm lines with "
                f"an average detection confidence of {confidence_score}%. "
                "The AI interpretation combines the detected line "
                "characteristics with traditional palmistry concepts "
                "for entertainment and self-reflection."
            ),

        "confidence": confidence_score,

        "fortune_score": fortune_score,

        "disclaimer":
            "Palmistry interpretations are for entertainment and self-reflection."
    }

# ============================================================
# TAROT READING
# ============================================================

def generate_tarot_reading(cards):
    """
    Generate Tarot Reading using AI.

    Falls back to dataset-based interpretation if AI fails.
    """

    prompt = f"""
You are an expert Tarot Interpretation Engine.

Cards:

{json.dumps(cards, indent=2)}

Generate a positive and insightful tarot reading.

IMPORTANT:

- Use the supplied cards.
- Do not claim supernatural certainty.
- Tarot is for entertainment and self-reflection.
- Return ONLY valid JSON.
- Do not return markdown.

Return exactly:

{{
    "overall_reading": "",
    "past": "",
    "present": "",
    "future": "",
    "advice": "",
    "lucky_elements": []
}}
"""

    try:
        response = ask_ai(prompt)

        if response:
            parsed = _parse_ai_json(response)

            if parsed:
                return parsed

    except Exception as e:
        print("AI Tarot Error:", e)

    # ========================================================
    # TAROT FALLBACK
    # ========================================================

    card_names = ", ".join(
        card.get("name", "Unknown")
        for card in cards
    )

    return {
        "overall_reading": (
            f"This reading is based on {card_names}. "
            "The cards can be used as a reflective tool "
            "for considering growth, choices and opportunities."
        ),

        "past": (
            "Past experiences may have provided useful lessons "
            "and resilience."
        ),

        "present": (
            "The present period encourages awareness, learning "
            "and thoughtful decisions."
        ),

        "future": (
            "Consistent effort and thoughtful choices may create "
            "positive opportunities."
        ),

        "advice": (
            "Stay patient, trust your abilities and remain open "
            "to new possibilities."
        ),

        "lucky_elements": [
            "Blue",
            "Green",
            "Thursday",
            "Innovation",
            "Learning",
            "Persistence"
        ]
    }