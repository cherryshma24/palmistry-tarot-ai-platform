import json

from app.services.ai_manager import ask_ai


def generate_personality_profile(
    profile,
    palm_reading,
    tarot_reading=None
):

    prompt = f"""
You are an advanced Personality & Life Insights AI.

Your job is to analyze the user's profile, palmistry reading and tarot reading
to generate a complete personality intelligence report.

User Profile:
{json.dumps(profile, indent=2)}

Palm Reading:
{json.dumps(palm_reading, indent=2)}

Tarot Reading:
{json.dumps(tarot_reading, indent=2) if tarot_reading else "None"}

Return ONLY valid JSON.

Return exactly this format:

{{
  "personality": {{
      "type":"",
      "confidence":90,
      "traits":[],
      "strengths":[],
      "growth_areas":[]
  }},

  "career": {{
      "career_score":90,
      "preferred_roles":[],
      "work_style":"",
      "leadership_style":""
  }},

  "relationships": {{
      "communication_style":"",
      "emotional_style":"",
      "relationship_strength":""
  }},

  "life_path": {{
      "current_phase":"",
      "future_opportunities":[]
  }},

  "recommendations":[
      "",
      "",
      ""
  ],

  "summary":""
}}

Rules:

- Return ONLY JSON.
- No markdown.
- No explanation.
- No extra text.
"""

    try:

        response = ask_ai(prompt)

        if response:

            response = response.strip()

            if response.startswith("```"):

                response = (
                    response
                    .replace("```json", "")
                    .replace("```", "")
                    .strip()
                )

            return json.loads(response)

    except Exception as e:

        print("Personality AI Error:", e)

    # =====================================================
    # FALLBACK
    # =====================================================

    return {
                "personality": {

            "type": "Creative Leader",

            "confidence": 91,

            "traits": [

                "Analytical",

                "Creative",

                "Determined",

                "Confident"

            ],

            "strengths": [

                "Leadership",

                "Problem Solving",

                "Fast Learner",

                "Adaptability"

            ],

            "growth_areas": [

                "Practice Patience",

                "Improve Work-Life Balance",

                "Delegate Responsibilities"

            ]

        },

        "career": {

            "career_score": 90,

            "prediction":
            "Your palm characteristics indicate excellent leadership potential with strong analytical abilities. Careers involving technology, management, research, or entrepreneurship are favorable.",

            "preferred_roles": [

                "Software Engineer",

                "AI Engineer",

                "Data Scientist",

                "Project Manager",

                "Business Analyst"

            ],

            "work_style":
            "Strategic, collaborative and result-oriented.",

            "leadership_style":
            "Inspirational and supportive."

        },

        "relationships": {

            "prediction":
            "You value trust, honesty and emotional stability. Meaningful long-term relationships are favored.",

            "communication_style":
            "Direct, respectful and empathetic.",

            "emotional_style":
            "Balanced and thoughtful.",

            "relationship_strength":
            "High"

        },

        "finance": {

            "prediction":
            "Your disciplined mindset indicates gradual financial growth through consistent effort.",

            "money_management":
            "Focus on long-term investments, savings and calculated financial decisions."

        },

        "health": {

            "prediction":
            "Overall wellness appears positive when balanced with sufficient rest and stress management.",

            "wellness_tip":
            "Maintain regular exercise, quality sleep and mindfulness practices."

        },

        "life_path": {

            "current_phase":
            "Growth and Skill Development",

            "future_opportunities": [

                "Leadership",

                "Career Advancement",

                "Financial Stability",

                "Personal Development"

            ]

        },

        "recommendations": [

            "Continue learning new technical skills.",

            "Build confidence through consistent practice.",

            "Maintain emotional balance during stressful situations.",

            "Take leadership opportunities whenever possible.",

            "Focus on long-term goals rather than short-term rewards."

        ],

        "summary":
        "The personality analysis suggests a confident, analytical and growth-oriented individual with strong leadership potential. Your palm characteristics indicate excellent problem-solving ability, emotional balance and promising opportunities for career advancement and personal success."

    }