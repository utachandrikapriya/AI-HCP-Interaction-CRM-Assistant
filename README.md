
# Project Title

A brief description of what this project does and who it's for

# 🩺 AI-Powered HCP CRM Interaction Assistant

> An AI-first Healthcare CRM Assistant built with **React, FastAPI, LangGraph, and Large Language Models (LLMs)** that enables Healthcare Professional (HCP) interaction logging entirely through natural language.

## 🌐 Live Demo

**🔗 Live Application:** https://ai-hcp-interaction-crm-assistant-ic.vercel.app/

---

## 📖 Overview

The AI-Powered HCP CRM Interaction Assistant is designed to simplify and automate the process of recording Healthcare Professional (HCP) interactions.

Instead of manually filling CRM forms, users simply describe their interaction in natural language through an AI chat interface. The AI extracts structured information, invokes LangGraph tools, and automatically updates the CRM form.

The application follows an **AI-first workflow**, ensuring that all interaction data is managed through intelligent agents rather than manual form editing.

---

# ✨ Features

- 🤖 AI-powered CRM form auto-population
- 💬 Natural language interaction logging
- ✏️ AI-driven editing of existing interaction fields
- 📄 Automatic professional CRM summary generation
- ✅ Form validation for missing information
- 📌 Intelligent follow-up action suggestions
- 🔄 LangGraph agent workflow with tool orchestration
- 🛡️ Simulation mode when API keys are unavailable
- 🎨 Modern split-screen responsive UI
- ⚡ FastAPI backend with React frontend

---

# 🖥️ Application Layout

The application consists of two primary panels.

## Left Panel

A structured Healthcare CRM interaction form containing fields such as:

- HCP Name
- Specialty
- Organization
- Interaction Type
- Interaction Date
- Products Discussed
- Topics Discussed
- Materials Shared
- Samples Distributed
- Follow-up Date
- Sentiment
- Interaction Outcome
- Executive Summary

> **Important:** Manual editing is intentionally disabled. The form can only be modified through AI interactions.

---

## Right Panel

An AI Assistant Chat interface where users interact using natural language.

Example:

```text
Yesterday I met Dr. Sarah Jenkins at General Hospital.

We discussed CardioLife.

The interaction was positive.

I shared one brochure.

Please log this interaction.
```

The AI automatically fills the CRM form.

---

# 🏗️ Architecture

```text
                 User
                   │
                   ▼
         AI Chat Interface (React)
                   │
                   ▼
              FastAPI Backend
                   │
                   ▼
            LangGraph Workflow
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
    LLM Reasoning        Tool Selection
        │                     │
        └──────────┬──────────┘
                   ▼
             LangGraph Tools
                   │
                   ▼
        SQLite Interaction State
                   │
                   ▼
        Auto-update CRM Form
```

---

# 🛠️ Technology Stack

## Frontend

- React (Vite)
- Redux Toolkit
- Vanilla CSS
- Lucide React

## Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite

## AI & Agent Framework

- LangGraph
- LangChain
- Google Gemini
- Groq
- OpenAI

---

# 🤖 LangGraph Tools

The application implements **five AI tools**.

---

## 1️⃣ Log Interaction Tool

Extracts structured information from natural language and populates the CRM form.

Example:

```text
Yesterday I met Dr. Sarah Jenkins.

We discussed CardioLife.

The interaction was positive.

I shared one brochure.
```

Automatically extracts:

- HCP Name
- Date
- Products
- Sentiment
- Materials Shared
- Summary

---

## 2️⃣ Edit Interaction Tool

Updates only requested fields while preserving existing information.

Example:

```text
Change the sentiment to Neutral.

Replace CardioLife with CardioMax.
```

Only the specified fields are modified.

---

## 3️⃣ Generate Summary Tool

Creates a professional CRM summary.

Example:

```text
Generate a CRM summary.
```

---

## 4️⃣ Validate Interaction Tool

Checks the form for missing or incomplete fields.

Example:

```text
Validate this interaction.
```

---

## 5️⃣ Suggest Follow-up Tool

Generates intelligent follow-up recommendations.

Example:

```text
Suggest follow-up tasks.
```

---

# 📂 Project Structure

```text
hcp-crm-assistant/
│
├── backend/
│   ├── app/
│   │   ├── agent.py
│   │   ├── database.py
│   │   ├── main.py
│   │   └── schemas.py
│   │
│   ├── requirements.txt
│   ├── test_agent.py
│   └── hcp_crm.db
│
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
├── README.md
└── .gitignore
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/Harish-Uta17/smart-hcp-logger.git

cd smart-hcp-logger
```

---

# Backend Setup

Move into backend

```bash
cd backend
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env`

```env
GOOGLE_API_KEY=your_google_api_key

# or

GROQ_API_KEY=your_groq_api_key

# or

OPENAI_API_KEY=your_openai_api_key
```

Run backend

```bash
uvicorn app.main:app --reload --port 8000
```

Backend runs on

```
http://localhost:8000
```

---

# Frontend Setup

Move into frontend

```bash
cd frontend
```

Install packages

```bash
npm install
```

Run frontend

```bash
npm run dev
```

Frontend runs on

```
http://localhost:5173
```

---

# 🧪 Test Backend

```bash
python test_agent.py
```

---

# 🌍 Deployment

## Live Demo

https://smart-hcp-logger-fxum.vercel.app/

---

# Example Workflow

### User

```text
Yesterday I met Dr. Sarah Jenkins.

We discussed CardioLife.

She was interested in clinical studies.

I shared a brochure.

Please log the interaction.
```

↓

AI selects

```
Log Interaction Tool
```

↓

CRM Form is automatically populated.

---

### User

```text
Actually change the sentiment to Neutral.
```

↓

AI selects

```
Edit Interaction Tool
```

↓

Only the sentiment field changes.

---

### User

```text
Generate summary.
```

↓

AI selects

```
Generate Summary Tool
```

---

### User

```text
Validate interaction.
```

↓

AI selects

```
Validate Interaction Tool
```

---

### User

```text
Suggest follow-up.
```

↓

AI selects

```
Suggest Follow-up Tool
```

---

# 📌 Key Highlights

- AI-first CRM experience
- No manual form filling
- LangGraph agent workflow
- LLM-powered reasoning
- Automatic tool selection
- Professional healthcare CRM automation
- Offline simulation fallback
- Clean React + FastAPI architecture

---

# 👨‍💻 Author

**Harish Kumar**

GitHub: https://github.com/utachandrikapriya/


---

# ⭐ Support

If you found this project helpful, consider giving it a ⭐ on GitHub!
