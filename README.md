# AI Lead Segmentation & Marketing Automation

An end-to-end AI-powered Lead Segmentation system that automatically classifies incoming leads, synchronizes them with Supabase and Brevo, and triggers personalized email marketing workflows.

---

## Overview

Marketing teams receive leads from multiple sources such as:

- Google Forms
- Facebook Lead Ads
- Landing Pages
- Events & Workshops
- CSV Imports

Without automatic segmentation, all leads receive the same follow-up process, resulting in low marketing efficiency.

This project uses a Machine Learning model to automatically classify each lead into predefined marketing segments, synchronize data with Supabase and Brevo, and trigger personalized email automation.

---

## Features

- AI-based Lead Segmentation using Random Forest
- Automatic Feature Engineering
- Real-time Prediction via FastAPI
- Batch Processing from raw data
- Supabase Integration
- Brevo Contact Synchronization
- Personalized Email Automation
- Support for Multiple Lead Sources

---

# System Architecture

```text
                    Multiple Lead Sources
      ┌─────────────────────────────────────────┐
      │                                         │
Google Form   Facebook Lead Ads   CSV Import   API
      │              │                │         │
      └──────────────┴────────────────┴─────────┘
                         │
                         ▼
              Feature Engineering
                         │
                         ▼
              Random Forest Classifier
                         │
                         ▼
               Lead Segmentation
                         │
          ┌──────────────┴──────────────┐
          │                             │
          ▼                             ▼
     Supabase Database             Brevo Contact
          │                             │
          └──────────────┬──────────────┘
                         ▼
                 Email Automation
```

> **TODO:** Add architecture diagram (Draw.io / Excalidraw)

---

# Project Structure

```text
.
├── api
│   ├── app.py
│   ├── pipeline.py
│   ├── process_raw_leads.py
│   ├── feature_engineering.py
│   ├── predict.py
│   ├── database.py
│   ├── brevo.py
│   └── config.py
│
├── models
│   └── random_forest_pipeline.pkl
│
├── notebooks
│   └── model_training.ipynb
│
├── data
│   ├── raw
│   └── processed
│
├── requirements.txt
└── README.md
```

---

# Machine Learning Pipeline

## Feature Engineering

The following features are automatically generated before prediction.

| Feature | Description |
|----------|-------------|
| COURSE_1 | Primary interested course |
| COURSE_2 | Secondary interested course |
| COURSE_3 | Third interested course |
| COURSE_COUNT | Number of selected courses |
| MULTI_COURSE | Whether multiple courses were selected |
| SOURCE_TYPE | CLUB / UNIVERSITY / SOCIAL / OTHER |
| REGISTER_MONTH | Registration month |
| REGISTER_DAY_OF_WEEK | Registration weekday |
| SCHOLARSHIP | Scholarship keyword detection |

---

## Model

**Algorithm**

```
Random Forest Classifier
```

**Prediction Target**

```
SEGMENT
```

Example predictions

```
BI_CLUB
BI_UNIVERSITY
DA_CLUB
DA_OTHER
BA_SOCIAL
BA_OTHER
AI_AGENT_CLUB
GENAI_UNIVERSITY
```

---

# Supported Segments

| Segment | Description |
|----------|-------------|
| BI_CLUB | Business Intelligence leads from clubs/events |
| BI_UNIVERSITY | Business Intelligence leads from universities |
| BA_SOCIAL | Business Analyst leads from social media |
| BA_OTHER | Business Analyst leads from other channels |
| DA_CLUB | Data Analytics leads from clubs/events |
| DA_OTHER | Data Analytics leads from other channels |
| AI_AGENT_CLUB | AI Agent workshop attendees |
| GENAI_UNIVERSITY | Generative AI university leads |

---