# AI-Powered HCP CRM Interaction Assistant

An AI-First CRM Healthcare Professional (HCP) Interaction Screen. This application provides a modern split-screen experience:
* **Left Panel**: A professional, structured CRM form detailing 18 fields of HCP interaction details. In accordance with requirements, this form is **disabled/read-only** for manual keyboard edits.
* **Right Panel**: A conversational AI chat assistant. Users communicate in natural language to log details, modify specific fields, generate summaries, validate fields, and suggest next actions. The AI agent automates these actions via LangGraph tools.

---

## 🛠️ Technology Stack
* **Frontend**: React (Vite), Redux Toolkit (state management), Vanilla CSS (premium dark-mode styling), Lucide React (vector icons).
* **Backend**: Python, FastAPI (web API framework), LangGraph (agent state graph orchestration), SQLAlchemy + SQLite (local database log state storage).
* **LLM Core**: LangChain wrappers supporting **Groq** (`gemma2-9b-it` or `llama-3.3-70b-versatile`), **Google Gemini** (`gemini-1.5-flash`), or **OpenAI** (`gpt-4o-mini`).
* **Resilient Dual-Mode Execution**:
  * **API Key Connected**: Runs the real LangGraph State Graph with tool calling.
  * **Simulation Active (Offline Fallback)**: If API keys are missing or the backend is offline, the frontend seamlessly engages an integrated simulation engine, demonstrating all 5 tools, updating fields, and returning chat feedback in real-time.

---

## 📦 Project Structure
```
hcp-crm-assistant/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── agent.py         # LangGraph workflow & tools (Log, Edit, Summarize, Validate, Suggest)
│   │   ├── database.py      # SQLite db models and helper transactions
│   │   ├── main.py          # FastAPI application routes
│   │   └── schemas.py       # Pydantic validation schemas
│   ├── requirements.txt     # Python backend dependencies
│   └── test_agent.py        # Independent backend validation script
└── frontend/
    ├── index.html           # HTML container
    ├── package.json         # Node.js dependencies
    ├── vite.config.js       # Vite configuration
    └── src/
        ├── main.jsx         # App mounting entrypoint
        ├── App.jsx          # Front-end UI (Split panels, suggestion pill actions, simulation fallback)
        ├── index.css        # Premium global dark-mode styles
        └── store/
            └── store.js     # Redux Toolkit global store and slices
```

---

## 🚀 Setup & Execution Instructions

### 1. Backend Server Setup
From the `backend/` directory:

1. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Keys (Optional)**:
   Create a `.env` file in the `backend/` directory:
   ```env
   # Choose one or more:
   GROQ_API_KEY=your_groq_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Start the FastAPI Backend Server**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   *The server runs locally at `http://localhost:8000`.*

4. **Verify backend tools (Unit Tests)**:
   ```bash
   python test_agent.py
   ```

### 2. Frontend React Client Setup
From the `frontend/` directory:

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Start the Vite Web Server**:
   ```bash
   npm run dev
   ```
   *Open your browser and navigate to `http://localhost:5173` to access the application.*

---

## 🤖 5 LangGraph Agent Tools Implemented

1. **Log Interaction Tool**: Parses natural language details to populate fields: HCP Name, Specialty, Organization, Interaction Type, Interaction Date, Products, Sentiment, Materials Shared, and Summary.
   * *Example prompt:* `"Yesterday I met Dr. Sarah Jenkins at General Hospital. We discussed CardioLife. Sentiment was positive. I shared one brochure."*
2. **Edit Interaction Tool**: Updates only specific requested fields (e.g. products, sentiment, specialty) while strictly preserving all other existing form data.
   * *Example prompt:* `"Actually, change the sentiment to Neutral and replace CardioLife with CardioMax."*
3. **Generate Summary Tool**: Uses the LLM (or fallback builder) to generate a concise, professional CRM paragraph describing the meeting, automatically writing it into the *CRM Executive Summary* field.
   * *Example prompt:* `"Generate a CRM summary of this interaction."*
4. **Validate Interaction Tool**: Reviews the active form for incomplete or missing fields, returning a structured checklist of what is missing.
   * *Example prompt:* `"Validate this interaction."*
5. **Suggest Follow-up Tool**: Analyzes the meeting context (sentiment, objections, products) to generate 3-4 professional follow-up actions.
   * *Example prompt:* `"Suggest some follow-up tasks."*
