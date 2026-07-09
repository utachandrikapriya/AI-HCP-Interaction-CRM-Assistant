import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ChatRequest, HCPInteractionSchema
from app.database import get_current_interaction, reset_current_interaction
from app.agent import run_agent_workflow

app = FastAPI(title="HCP Interaction Assistant CRM Backend")

# Allow requests from React frontend (e.g. http://localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "running", "service": "HCP CRM Interaction API"}

@app.get("/api/interaction")
def get_interaction():
    """Gets the current CRM form interaction state."""
    return get_current_interaction()

@app.post("/api/reset")
def reset_interaction():
    """Resets the CRM form state to empty default values."""
    return reset_current_interaction()

@app.post("/api/chat")
def post_chat(payload: ChatRequest):
    """Processes user message through the LangGraph agent/simulation,
    running the selected tools and returning the chatbot response and form state.
    """
    result = run_agent_workflow(payload.message, payload.history)
    return {
        "response": result["response"],
        "toolTriggered": result["tool_triggered"],
        "formState": result["form_state"]
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
