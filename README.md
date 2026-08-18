# 🔮 Palmistry & Tarot AI

An AI-powered Palmistry and Tarot Intelligence Platform that combines computer vision, palm feature analysis, tarot interpretation, personality intelligence, and AI-generated reports in a unified web application.

> **Note:** Palmistry and Tarot interpretations are intended for entertainment and self-reflection only. They should not be treated as medical, financial, legal, or professional advice.

---

## 📌 Project Overview

**Palmistry & Tarot AI** is a full-stack web application designed to provide intelligent spiritual and self-reflective insights from:

- Palm images
- Palm lines and hand features
- Tarot card selections
- User profile information

The platform uses computer vision techniques to process palm images and an AI interpretation layer to transform the extracted information into readable insights and reports.

The system provides separate intelligence modules for:

- 🖐️ Palm Analysis
- 🃏 Tarot Intelligence
- 🧠 Personality Intelligence
- 🤖 AI Interpretation
- 📊 Report Generation

---

## ✨ Key Features

### 🖐️ Palm Analysis

Users can upload a palm image for analysis.

The system performs:

- Palm image preprocessing
- Image enhancement
- Hand landmark detection
- Palm feature extraction
- Palm line analysis
- Palm shape classification
- AI-based interpretation

The system can analyze major palm features such as:

- Life Line
- Head Line
- Heart Line
- Fate Line
- Palm dimensions
- Finger dimensions
- Hand orientation
- Palm proportions

---

### 🃏 Tarot Intelligence

The Tarot module provides:

- Tarot card selection
- Single-card readings
- Card information
- Arcana classification
- Suit information
- Keywords
- Fortune-telling meanings
- Light meanings
- AI-generated interpretation

The project uses a Tarot dataset containing the 78 traditional Tarot cards.

---

### 🧠 Personality Intelligence

The platform generates a personality-oriented interpretation based on the available analysis data.

The personality module can provide:

- Personality type
- Strengths
- Weaknesses
- Behavioral traits
- Communication style
- Leadership style
- Emotional style
- Personal growth suggestions
- Overall personality summary

---

### 🤖 AI Interpretation

The AI layer converts structured analysis information into natural-language insights.

The project uses:

- OpenRouter API
- Google Gemma model
- Structured prompts
- JSON-based AI responses
- Fallback interpretation logic

The AI receives structured analysis data instead of directly guessing information from an image.

---

### 📊 Intelligent Reports

The application combines analysis results and AI interpretation into user-friendly reports.

Reports can contain:

- AI Summary
- Palm Analysis
- Personality Profile
- Tarot Interpretation
- Career Intelligence
- Relationship Insights
- Financial Outlook
- Health & Wellness themes
- Personal Growth
- Recommendations
- Overall Summary
- Confidence/Fortune information

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │      User            │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   React Frontend     │
                    │      + Vite           │
                    └──────────┬───────────┘
                               │
                         REST API
                               │
                               ▼
                    ┌──────────────────────┐
                    │    FastAPI Backend   │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      ┌────────────┐    ┌────────────┐    ┌────────────┐
      │    Palm    │    │   Tarot    │    │ Personality│
      │  Analysis  │    │ Intelligence│   │ Intelligence│
      └─────┬──────┘    └─────┬──────┘    └─────┬──────┘
            │                 │                 │
            ▼                 │                 │
     ┌──────────────┐         │                 │
     │ OpenCV       │         │                 │
     │ MediaPipe    │         │                 │
     │ YOLO         │         │                 │
     └──────┬───────┘         │                 │
            │                 │                 │
            └─────────────────┼─────────────────┘
                              ▼
                    ┌──────────────────────┐
                    │   AI Interpretation  │
                    │      OpenRouter      │
                    │      Gemma Model     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ PostgreSQL Database  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Generated Report   │
                    └──────────────────────┘