# System Architecture

## 1. Architecture Overview

The Palmistry & Tarot Intelligence Platform follows a full-stack architecture consisting of a React frontend, FastAPI backend, computer vision and machine learning components, AI interpretation services, and a PostgreSQL database.

```text
User
 │
 ▼
React + Vite Frontend
 │
 │ REST API
 ▼
FastAPI Backend
 │
 ├── Authentication
 ├── Palm Analysis
 ├── Tarot Intelligence
 ├── Personality Intelligence
 ├── Reports
 └── Dashboard
 │
 ├───────────────┬────────────────┐
 ▼               ▼                ▼
Computer       Tarot           Personality
Vision         Engine          Intelligence
 │
 ├── OpenCV
 ├── MediaPipe
 └── YOLO
 │
 ▼
Structured Analysis Data
 │
 ▼
OpenRouter AI
 │
 ▼
AI Interpretation
 │
 ▼
Generated Report
 │
 ▼
PostgreSQL Database