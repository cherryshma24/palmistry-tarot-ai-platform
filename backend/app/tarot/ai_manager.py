import json

from app.services.openrouter_service import ask_ai


# ============================================================
# HELPER — CLEAN AI JSON RESPONSE
# ============================================================

def _parse_ai_json(response):
    """
    Convert an AI response into a Python dictionary.

    Handles:
    - Normal JSON
    - JSON wrapped in ```json
    - JSON wrapped in ```
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

    try:
        return json.loads(response)
    except json.JSONDecodeError as e:
        print("AI JSON Parse Error:", e)
        return None


# ============================================================
# HELPER — NORMALIZE SCORE
# ============================================================

def _normalize_score(value, default=0):
    """
    Convert an AI-generated score into a clean number from 0-100.

    Examples:
        78      -> 78
        "78"    -> 78
        "78%"   -> 78
        7.5     -> 7.5
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
    Normalize AI palm reading using actual YOLO line detection data.

    CV measurements:
        - confidence_percent
        - length_pixels
        - angle_degrees
        - curvature_degrees

    are ALWAYS taken from YOLO.

    Career and fortune scores are calculated from
    actual detected line confidence values.
    """

    if not isinstance(reading, dict):
        return None

    # ========================================================
    # GET LINE DETECTION DATA
    # ========================================================

    line_data = palm_features.get("line_detection", {})

    if not isinstance(line_data, dict):
        line_data = {}

    # ========================================================
    # GET AI PALM ANALYSIS
    # ========================================================

    palm_analysis = reading.get("palm_analysis", {})

    if not isinstance(palm_analysis, dict):
        palm_analysis = {}

    # ========================================================
    # FORCE REAL YOLO VALUES
    # ========================================================

    for line_name in [
        "life",
        "heart",
        "head",
        "fate"
    ]:

        actual = line_data.get(line_name, {})

        if not isinstance(actual, dict):
            actual = {}

        ai_line = palm_analysis.get(
            f"{line_name}_line",
            {}
        )

        if not isinstance(ai_line, dict):
            ai_line = {}

        # REAL YOLO VALUES ONLY

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

    # ========================================================
    # GET REAL LINE CONFIDENCES
    # ========================================================

    def get_confidence(line_name):

        line = line_data.get(
            line_name,
            {}
        )

        if not isinstance(line, dict):
            return 0.0

        try:
            value = float(
                line.get(
                    "confidence_percent",
                    0
                )
            )
        except (ValueError, TypeError):
            return 0.0

        return max(
            0.0,
            min(
                100.0,
                value
            )
        )

    life_conf = get_confidence("life")
    heart_conf = get_confidence("heart")
    head_conf = get_confidence("head")
    fate_conf = get_confidence("fate")

    # ========================================================
    # OVERALL CV CONFIDENCE
    # ========================================================

    line_confidences = [
        life_conf,
        heart_conf,
        head_conf,
        fate_conf
    ]

    actual_confidence = (
        sum(line_confidences)
        / len(line_confidences)
    )

    actual_confidence = round(
        max(
            0.0,
            min(
                100.0,
                actual_confidence
            )
        ),
        1
    )

    # ========================================================
    # CAREER SCORE
    # ========================================================

    career_score = (
        head_conf * 0.35
        + life_conf * 0.25
        + heart_conf * 0.25
        + fate_conf * 0.15
    )

    career_score = round(
        max(
            0.0,
            min(
                100.0,
                career_score
            )
        ),
        1
    )

    # ========================================================
    # SAVE CAREER SCORE
    # ========================================================

    career = reading.get(
        "career",
        {}
    )

    if not isinstance(career, dict):
        career = {}

    career["career_score"] = career_score

    reading["career"] = career

    # ========================================================
    # FORTUNE SCORE
    # ========================================================

    fortune_score = (
        life_conf * 0.30
        + heart_conf * 0.30
        + head_conf * 0.25
        + fate_conf * 0.15
    )

    fortune_score = round(
        max(
            0.0,
            min(
                100.0,
                fortune_score
            )
        ),
        1
    )

    reading["fortune_score"] = fortune_score

    # ========================================================
    # FORCE CORRECT OVERALL CONFIDENCE
    # ========================================================

    reading["confidence"] = actual_confidence

    # ========================================================
    # CORRECT OVERALL SUMMARY
    # ========================================================

    reading["overall_summary"] = (
        "Computer vision detected the major palm lines "
        f"with an average detection confidence of "
        f"{actual_confidence}%. "
        "The AI interpretation combines the detected "
        "palm characteristics with traditional palmistry "
        "concepts for entertainment and self-reflection."
    )

    # ========================================================
    # DISCLAIMER
    # ========================================================

    reading["disclaimer"] = (
        "Palmistry interpretations are for entertainment "
        "and self-reflection."
    )

    # ========================================================
    # DEBUG OUTPUT
    # ========================================================

    print("\n========== PALM SCORE DEBUG ==========")
    print("Life confidence :", life_conf)
    print("Heart confidence:", heart_conf)
    print("Head confidence :", head_conf)
    print("Fate confidence :", fate_conf)
    print("Overall CV      :", actual_confidence)
    print("Career score    :", career_score)
    print("Fortune score   :", fortune_score)
    print("======================================\n")

    return reading

    
               
    
    

# ============================================================
# PALM READING
# ============================================================

def generate_palm_reading(profile, palm_features):
    """
    Generate AI-powered Palm Reading.

    Uses:
        YOLOv8 Pose
        OpenCV
        MediaPipe
        OpenRouter

    The actual computer-vision measurements are preserved.
    """

    analysis_payload = {
        "profile": profile,
        "palm_features": palm_features,
        "system": {
            "platform": (
                "Palmistry & Tarot Intelligence Platform"
            ),
            "cv_engine": (
                "MediaPipe + OpenCV + YOLOv8 Pose"
            ),
            "ai_engine": "OpenRouter"
        }
    }

    # ========================================================
    # AI PROMPT
    # ========================================================

    prompt = f"""
You are the AI Palmistry Interpretation Engine of a
Palmistry & Tarot Intelligence Platform.

Your task is to interpret palm-line features detected by
a computer-vision system.

IMPORTANT RULES:

1. Use ONLY the supplied palm_features.
2. Do NOT invent measurements.
3. Do NOT change any computer-vision measurements.
4. Do NOT change confidence percentages.
5. The confidence percentage represents computer-vision
   detection confidence, NOT certainty of palmistry.
6. If a line has low detection confidence, clearly state
   that the interpretation is uncertain.
7. Do NOT make medical diagnoses.
8. Do NOT make guaranteed financial predictions.
9. Do NOT make guaranteed future predictions.
10. Palmistry is for entertainment and self-reflection.
11. Use a positive, professional and natural tone.
12. Return ONLY valid JSON.
13. Do NOT return markdown.
14. Do NOT add explanations outside the JSON.

VERY IMPORTANT:

The following values come from the computer-vision model:

- Life line confidence
- Heart line confidence
- Head line confidence
- Fate line confidence
- Line lengths
- Line angles
- Line curvature

You MUST preserve these values.

DO NOT invent new confidence percentages.

INPUT DATA:

{json.dumps(analysis_payload, indent=2)}

Return exactly this JSON structure:

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
        "career_score": null
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

    "confidence": null,

    "fortune_score": null,

    "disclaimer":
        "Palmistry interpretations are for entertainment and self-reflection."
}}

SCORING:

- confidence must represent computer-vision quality.
- Do NOT artificially increase confidence.
- fortune_score is an entertainment/self-reflection score.
- Do NOT claim that fortune_score is scientifically predictive.
"""

    # ========================================================
    # CALL OPENROUTER
    # ========================================================

    try:

        response = ask_ai(prompt)

        if response:

            parsed = _parse_ai_json(
                response
            )

            if parsed:

                normalized = _normalize_palm_reading(
                    parsed,
                    palm_features
                )

                if normalized:
                    return normalized

    except Exception as e:

        print(
            "AI Palm Reading Error:",
            e
        )

    # ========================================================
    # FALLBACK
    # ========================================================

    print(
        "Using rule-based palm reading fallback."
    )

    return _generate_palm_fallback(
        palm_features
    )


# ============================================================
# PALM FALLBACK
# ============================================================

def _generate_palm_fallback(palm_features):
    """
    Generate a safe fallback reading using actual
    computer-vision palm-line information.
    """

    # --------------------------------------------------------
    # Get line
    # --------------------------------------------------------

    def get_line(name):

        # Preferred location
        line_data = palm_features.get(
            "line_detection",
            {}
        )

        if isinstance(line_data, dict):

            value = line_data.get(
                name,
                {}
            )

            if isinstance(value, dict):
                return value

        # Compatibility with older structures
        value = palm_features.get(
            name,
            {}
        )

        if isinstance(value, dict):
            return value

        value = palm_features.get(
            f"{name}_line",
            {}
        )

        if isinstance(value, dict):
            return value

        return {}

    life = get_line("life")
    heart = get_line("heart")
    head = get_line("head")
    fate = get_line("fate")

    # --------------------------------------------------------
    # Confidence
    # --------------------------------------------------------

    life_conf = float(
        life.get(
            "confidence_percent",
            0
        )
    )

    heart_conf = float(
        heart.get(
            "confidence_percent",
            0
        )
    )

    head_conf = float(
        head.get(
            "confidence_percent",
            0
        )
    )

    fate_conf = float(
        fate.get(
            "confidence_percent",
            0
        )
    )

    # --------------------------------------------------------
    # Overall confidence
    # --------------------------------------------------------

    confidence_score = round(
        (
            life_conf
            + heart_conf
            + head_conf
            + fate_conf
        ) / 4,
        1
    )

    confidence_score = max(
        0,
        min(
            100,
            confidence_score
        )
    )

    # --------------------------------------------------------
    # Entertainment score
    # --------------------------------------------------------

    fortune_score = round(
        (
            life_conf * 0.30
            + heart_conf * 0.30
            + head_conf * 0.25
            + fate_conf * 0.15
        ),
        1
    )

    fortune_score = max(
        0,
        min(
            100,
            fortune_score
        )
    )

    # ========================================================
    # RETURN FALLBACK
    # ========================================================

    return {

        "personality": {

            "traits": [
                "Curious",
                "Adaptable",
                "Empathetic",
                "Observant"
            ],

            "strengths": [
                "Analytical thinking",
                "Emotional awareness",
                "Communication skills"
            ],

            "growth_areas": [
                "Maintain consistent focus",
                "Develop long-term clarity",
                "Balance flexibility with planning"
            ]
        },

        "palm_analysis": {

            "life_line": {

                "confidence_percent":
                    life_conf,

                "length_pixels":
                    life.get(
                        "length_pixels",
                        0
                    ),

                "angle_degrees":
                    life.get(
                        "angle_degrees",
                        0
                    ),

                "curvature_degrees":
                    life.get(
                        "average_curvature_degrees",
                        0
                    ),

                "interpretation":
                    (
                        "The detected life line has "
                        "characteristics traditionally "
                        "associated with resilience, "
                        "adaptability and steady growth."
                    ),

                "key_observations": [
                    "Life line detected",
                    f"Detection confidence: {life_conf}%"
                ]
            },

            "heart_line": {

                "confidence_percent":
                    heart_conf,

                "length_pixels":
                    heart.get(
                        "length_pixels",
                        0
                    ),

                "angle_degrees":
                    heart.get(
                        "angle_degrees",
                        0
                    ),

                "curvature_degrees":
                    heart.get(
                        "average_curvature_degrees",
                        0
                    ),

                "interpretation":
                    (
                        "The detected heart line is "
                        "traditionally associated with "
                        "emotional awareness, warmth "
                        "and meaningful connections."
                    ),

                "key_observations": [
                    "Heart line detected",
                    f"Detection confidence: {heart_conf}%"
                ]
            },

            "head_line": {

                "confidence_percent":
                    head_conf,

                "length_pixels":
                    head.get(
                        "length_pixels",
                        0
                    ),

                "angle_degrees":
                    head.get(
                        "angle_degrees",
                        0
                    ),

                "curvature_degrees":
                    head.get(
                        "average_curvature_degrees",
                        0
                    ),

                "interpretation":
                    (
                        "The detected head line is "
                        "traditionally associated with "
                        "thoughtful analysis, practical "
                        "thinking and flexibility."
                    ),

                "key_observations": [
                    "Head line detected",
                    f"Detection confidence: {head_conf}%"
                ]
            },

            "fate_line": {

                "confidence_percent":
                    fate_conf,

                "length_pixels":
                    fate.get(
                        "length_pixels",
                        0
                    ),

                "angle_degrees":
                    fate.get(
                        "angle_degrees",
                        0
                    ),

                "curvature_degrees":
                    fate.get(
                        "average_curvature_degrees",
                        0
                    ),

                "interpretation":
                    (
                        "The fate line was detected with "
                        f"{fate_conf}% confidence. "
                        "Because the detection confidence "
                        "is low, this interpretation should "
                        "be treated cautiously."
                    ),

                "key_observations": [
                    "Fate line detected",
                    f"Detection confidence: {fate_conf}%"
                ]
            }
        },

        "career": {

            "prediction":
                (
                    "The detected palm characteristics "
                    "can be viewed traditionally as "
                    "supporting persistence, communication "
                    "and adaptable thinking."
                ),

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
                (
                    "The heart-line characteristics are "
                    "traditionally associated with emotional "
                    "awareness and meaningful connections."
                ),

            "compatibility":
                (
                    "Open communication, honesty and "
                    "mutual respect can support healthy "
                    "relationships."
                )
        },

        "finance": {

            "prediction":
                (
                    "Palmistry cannot predict financial "
                    "outcomes. Use real-world planning "
                    "and informed decisions."
                ),

            "money_management":
                (
                    "Consider budgeting, disciplined "
                    "saving and thoughtful spending."
                )
        },

        "health": {

            "prediction":
                (
                    "Palm lines cannot reliably determine "
                    "health conditions."
                ),

            "wellness_tip":
                (
                    "Maintain healthy habits and consult "
                    "qualified professionals for health "
                    "concerns."
                )
        },

        "recommendations": [

            "Keep a journal for self-reflection.",
            "Develop consistent long-term goals.",
            "Continue developing your technical and creative skills.",
            "Maintain healthy work-life balance."
        ],

        "overall_summary":
            (
                "Computer vision detected the major palm "
                "lines with an average detection confidence "
                f"of {confidence_score}%. The interpretation "
                "combines the detected characteristics with "
                "traditional palmistry concepts for "
                "entertainment and self-reflection."
            ),

        "confidence":
            confidence_score,

        "fortune_score":
            fortune_score,

        "disclaimer":
            (
                "Palmistry interpretations are for "
                "entertainment and self-reflection."
            )
    }


# ============================================================
# TAROT READING
# ============================================================

def generate_tarot_reading(cards):
    """
    Generate AI-powered Tarot Reading.

    Falls back to a simple dataset-based interpretation
    if OpenRouter fails.
    """

    prompt = f"""
You are an expert Tarot Interpretation Engine.

Cards:

{json.dumps(cards, indent=2)}

Generate a positive, insightful and natural tarot reading.

IMPORTANT:

1. Use the supplied cards.
2. Do not claim supernatural certainty.
3. Tarot is for entertainment and self-reflection.
4. Do not make guaranteed predictions.
5. Return ONLY valid JSON.
6. Do not return markdown.

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

    # ========================================================
    # CALL OPENROUTER
    # ========================================================

    try:

        response = ask_ai(
            prompt
        )

        if response:

            parsed = _parse_ai_json(
                response
            )

            if parsed:
                return parsed

    except Exception as e:

        print(
            "AI Tarot Error:",
            e
        )

    # ========================================================
    # TAROT FALLBACK
    # ========================================================

    card_names = ", ".join(
        card.get(
            "name",
            "Unknown"
        )
        for card in cards
    )

    return {

        "overall_reading":
            (
                f"This reading is based on "
                f"{card_names}. The cards can be "
                "used as a reflective tool for "
                "considering growth, choices and "
                "opportunities."
            ),

        "past":
            (
                "Past experiences may have provided "
                "useful lessons and resilience."
            ),

        "present":
            (
                "The present encourages awareness, "
                "learning and thoughtful decisions."
            ),

        "future":
            (
                "Consistent effort and thoughtful "
                "choices may create positive opportunities."
            ),

        "advice":
            (
                "Stay patient, trust your abilities "
                "and remain open to new possibilities."
            ),

        "lucky_elements": [
            "Blue",
            "Green",
            "Thursday",
            "Learning",
            "Persistence"
        ]
    }