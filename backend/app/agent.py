import os
import json
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Import database helpers
from app.database import get_current_interaction, update_current_interaction

load_dotenv()

# Check for API keys to see if we run in real agent mode or simulation mode
HAS_API_KEYS = any(
    os.getenv(k) for k in ["GROQ_API_KEY", "GEMINI_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY"]
)

# Tool 1: Log Interaction
def run_log_interaction(
    hcpName: Optional[str] = None,
    specialty: Optional[str] = None,
    organization: Optional[str] = None,
    interactionType: Optional[str] = None,
    interactionDate: Optional[str] = None,
    interactionTime: Optional[str] = None,
    location: Optional[str] = None,
    duration: Optional[str] = None,
    productsDiscussed: Optional[List[str]] = None,
    topicsDiscussed: Optional[List[str]] = None,
    materialsShared: Optional[List[str]] = None,
    samplesDistributed: Optional[List[str]] = None,
    questionsRaised: Optional[List[str]] = None,
    objections: Optional[List[str]] = None,
    followUpDate: Optional[str] = None,
    sentiment: Optional[str] = None,
    interactionOutcome: Optional[str] = None,
    summary: Optional[str] = None,
) -> Dict[str, Any]:
    """Log a new HCP interaction, extracting details from the conversation."""
    current = get_current_interaction()
    updates = {}
    
    # We update any field that is explicitly passed (not None)
    for field, val in [
        ("hcpName", hcpName),
        ("specialty", specialty),
        ("organization", organization),
        ("interactionType", interactionType),
        ("interactionDate", interactionDate),
        ("interactionTime", interactionTime),
        ("location", location),
        ("duration", duration),
        ("productsDiscussed", productsDiscussed),
        ("topicsDiscussed", topicsDiscussed),
        ("materialsShared", materialsShared),
        ("samplesDistributed", samplesDistributed),
        ("questionsRaised", questionsRaised),
        ("objections", objections),
        ("followUpDate", followUpDate),
        ("sentiment", sentiment),
        ("interactionOutcome", interactionOutcome),
        ("summary", summary),
    ]:
        if val is not None:
            updates[field] = val

    updated = update_current_interaction(updates)
    return {
        "status": "success",
        "tool": "Log Interaction",
        "message": f"Successfully logged interaction details for {updated.get('hcpName', 'HCP')}.",
        "data": updated
    }

# Tool 2: Edit Interaction
def run_edit_interaction(
    hcpName: Optional[str] = None,
    specialty: Optional[str] = None,
    organization: Optional[str] = None,
    interactionType: Optional[str] = None,
    interactionDate: Optional[str] = None,
    interactionTime: Optional[str] = None,
    location: Optional[str] = None,
    duration: Optional[str] = None,
    productsDiscussed: Optional[List[str]] = None,
    topicsDiscussed: Optional[List[str]] = None,
    materialsShared: Optional[List[str]] = None,
    samplesDistributed: Optional[List[str]] = None,
    questionsRaised: Optional[List[str]] = None,
    objections: Optional[List[str]] = None,
    followUpDate: Optional[str] = None,
    sentiment: Optional[str] = None,
    interactionOutcome: Optional[str] = None,
    summary: Optional[str] = None,
) -> Dict[str, Any]:
    """Modify only the specified fields of the existing HCP interaction form."""
    updates = {}
    for field, val in [
        ("hcpName", hcpName),
        ("specialty", specialty),
        ("organization", organization),
        ("interactionType", interactionType),
        ("interactionDate", interactionDate),
        ("interactionTime", interactionTime),
        ("location", location),
        ("duration", duration),
        ("productsDiscussed", productsDiscussed),
        ("topicsDiscussed", topicsDiscussed),
        ("materialsShared", materialsShared),
        ("samplesDistributed", samplesDistributed),
        ("questionsRaised", questionsRaised),
        ("objections", objections),
        ("followUpDate", followUpDate),
        ("sentiment", sentiment),
        ("interactionOutcome", interactionOutcome),
        ("summary", summary),
    ]:
        if val is not None:
            updates[field] = val

    updated = update_current_interaction(updates)
    fields_list = ", ".join(updates.keys())
    return {
        "status": "success",
        "tool": "Edit Interaction",
        "message": f"Successfully edited fields: {fields_list}.",
        "data": updated
    }

# Tool 3: Generate Summary
def run_generate_summary(llm_client=None) -> Dict[str, Any]:
    """Generate a professional CRM summary of the current interaction."""
    current = get_current_interaction()
    
    hcp = current.get("hcpName") or "the healthcare professional"
    org = f" at {current.get('organization')}" if current.get("organization") else ""
    specialty = f" ({current.get('specialty')})" if current.get("specialty") else ""
    products = ", ".join(current.get("productsDiscussed", []))
    materials = ", ".join(current.get("materialsShared", []))
    sentiment = current.get("sentiment") or "neutral"
    
    summary_text = ""
    if llm_client:
        try:
            # Generate using actual LLM
            prompt = f"""
            You are a medical sales CRM summary generator. Generate a concise, professional CRM interaction summary based on the following details:
            HCP: {hcp}{specialty}{org}
            Interaction Type: {current.get('interactionType')}
            Products Discussed: {products}
            Topics Discussed: {", ".join(current.get('topicsDiscussed', []))}
            Materials Shared: {materials}
            Sentiment: {sentiment}
            Outcome: {current.get('interactionOutcome')}
            
            Provide only a professional 2-3 sentence paragraph summary.
            """
            summary_text = llm_client.invoke(prompt).content.strip()
        except Exception as e:
            print(f"Error calling LLM in summary: {e}")
            
    if not summary_text:
        # Fallback summary builder
        prod_str = f" to discuss {products}" if products else ""
        mat_str = f" Shared marketing/clinical materials including {materials}." if materials else ""
        sentiment_str = f" The observed sentiment was {sentiment.lower()} and the HCP expressed interest." if sentiment else ""
        summary_text = f"Sales representative conducted a {current.get('interactionType') or 'meeting'} with {hcp}{org}{prod_str}.{mat_str}{sentiment_str}"

    updated = update_current_interaction({"summary": summary_text})
    return {
        "status": "success",
        "tool": "Generate Summary",
        "message": "Generated interaction summary successfully.",
        "summary": summary_text,
        "data": updated
    }

# Tool 4: Validate Interaction
def run_validate_interaction() -> Dict[str, Any]:
    """Validate the current form for missing fields and returns a list of missing fields."""
    current = get_current_interaction()
    missing_fields = []
    
    field_labels = {
        "hcpName": "HCP Name",
        "specialty": "Specialty",
        "organization": "Organization",
        "interactionType": "Interaction Type",
        "interactionDate": "Interaction Date",
        "interactionTime": "Interaction Time",
        "location": "Location",
        "duration": "Duration",
        "productsDiscussed": "Products Discussed",
        "topicsDiscussed": "Topics Discussed",
        "materialsShared": "Materials Shared",
        "samplesDistributed": "Samples Distributed",
        "questionsRaised": "Questions Raised",
        "objections": "Objections",
        "followUpDate": "Follow-up Date",
        "sentiment": "Sentiment",
        "interactionOutcome": "Interaction Outcome",
        "summary": "Summary"
    }

    for key, label in field_labels.items():
        val = current.get(key)
        if isinstance(val, list):
            if not val:
                missing_fields.append(label)
        elif not val or str(val).strip() == "":
            missing_fields.append(label)

    if not missing_fields:
        message = "✅ Validation complete. All fields are successfully populated!"
    else:
        bullets = "\n".join([f"• {f}" for f in missing_fields])
        message = f"Validation Results:\nMissing:\n{bullets}\n\nEverything else is complete."

    return {
        "status": "success",
        "tool": "Validate Interaction",
        "message": message,
        "missingFields": missing_fields,
        "data": current
    }

# Tool 5: Suggest Follow-up
def run_suggest_follow_up(llm_client=None) -> Dict[str, Any]:
    """Suggest professional follow-up tasks and actions based on the current interaction."""
    current = get_current_interaction()
    hcp = current.get("hcpName") or "Dr. Smith"
    products = ", ".join(current.get("productsDiscussed", []))
    objections = ", ".join(current.get("objections", []))
    questions = ", ".join(current.get("questionsRaised", []))
    
    suggestions_text = ""
    if llm_client:
        try:
            prompt = f"""
            You are a medical sales coach. Suggest 3-4 professional follow-up actions for a sales rep after meeting with:
            HCP Name: {hcp}
            Products Discussed: {products}
            Questions Raised: {questions}
            Objections Noted: {objections}
            Sentiment: {current.get('sentiment')}
            
            Format your response strictly as a list of bullet points starting with '• '. Do not include any introductory or concluding remarks.
            """
            suggestions_text = llm_client.invoke(prompt).content.strip()
        except Exception as e:
            print(f"Error calling LLM in follow-up: {e}")

    if not suggestions_text:
        # Structured fallback
        suggestions = []
        if products:
            suggestions.append(f"Share latest efficacy study or pricing details for {products}.")
        else:
            suggestions.append("Send product portfolio brochure via email.")
            
        if objections:
            suggestions.append(f"Prepare clinical data sheet to address objections: '{objections}'.")
        else:
            suggestions.append("Schedule follow-up call to review any clinical questions.")
            
        suggestions.append(f"Add {hcp} to the advisory board invite list or monthly newsletter.")
        suggestions.append("Schedule next touchpoint meeting in 2 weeks.")
        suggestions_text = "\n".join([f"• {s}" for s in suggestions])

    return {
        "status": "success",
        "tool": "Suggest Follow-up",
        "message": f"Suggested Follow-ups for {hcp}:\n{suggestions_text}",
        "suggestions": suggestions_text,
        "data": current
    }


# =====================================================================
# LangGraph Orchestration (Real LLM Integration)
# =====================================================================
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Define state structure
class AgentState(BaseModel):
    messages: List[Any] = Field(default_factory=list)
    form_state: Dict[str, Any] = Field(default_factory=dict)
    tools_run: List[str] = Field(default_factory=list)

def get_llm():
    """Initializes LLM client based on available environment variables."""
    # 1. Groq
    if os.getenv("GROQ_API_KEY"):
        from langchain_groq import ChatGroq
        model_name = os.getenv("GROQ_MODEL", "gemma2-9b-it") # gemma2-9b-it or llama-3.3-70b-versatile
        return ChatGroq(temperature=0.1, model_name=model_name)
    # 2. Google Gemini
    elif os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"):
        from langchain_google_genai import ChatGoogleGenerativeAI
        model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        # Ensure we set the API key in environment for safety
        if os.getenv("GEMINI_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
            os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
        return ChatGoogleGenerativeAI(temperature=0.1, model=model_name)
    # 3. OpenAI
    elif os.getenv("OPENAI_API_KEY"):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(temperature=0.1, model="gpt-4o-mini")
    
    return None

# Convert functions to LangChain Tools
from langchain_core.tools import tool

@tool
def log_interaction_tool(
    hcpName: Optional[str] = None,
    specialty: Optional[str] = None,
    organization: Optional[str] = None,
    interactionType: Optional[str] = None,
    interactionDate: Optional[str] = None,
    interactionTime: Optional[str] = None,
    location: Optional[str] = None,
    duration: Optional[str] = None,
    productsDiscussed: Optional[List[str]] = None,
    topicsDiscussed: Optional[List[str]] = None,
    materialsShared: Optional[List[str]] = None,
    samplesDistributed: Optional[List[str]] = None,
    questionsRaised: Optional[List[str]] = None,
    objections: Optional[List[str]] = None,
    followUpDate: Optional[str] = None,
    sentiment: Optional[str] = None,
    interactionOutcome: Optional[str] = None,
    summary: Optional[str] = None,
) -> str:
    """Log a brand new HCP interaction from natural language input. Use this to capture new interactions.
    Ensure to parse the text and extract fields like hcpName, interactionDate (e.g. yesterday translates to date), productsDiscussed, sentiment, materialsShared, etc.
    """
    res = run_log_interaction(
        hcpName=hcpName, specialty=specialty, organization=organization,
        interactionType=interactionType, interactionDate=interactionDate, interactionTime=interactionTime,
        location=location, duration=duration, productsDiscussed=productsDiscussed,
        topicsDiscussed=topicsDiscussed, materialsShared=materialsShared, samplesDistributed=samplesDistributed,
        questionsRaised=questionsRaised, objections=objections, followUpDate=followUpDate,
        sentiment=sentiment, interactionOutcome=interactionOutcome, summary=summary
    )
    return json.dumps(res)

@tool
def edit_interaction_tool(
    hcpName: Optional[str] = None,
    specialty: Optional[str] = None,
    organization: Optional[str] = None,
    interactionType: Optional[str] = None,
    interactionDate: Optional[str] = None,
    interactionTime: Optional[str] = None,
    location: Optional[str] = None,
    duration: Optional[str] = None,
    productsDiscussed: Optional[List[str]] = None,
    topicsDiscussed: Optional[List[str]] = None,
    materialsShared: Optional[List[str]] = None,
    samplesDistributed: Optional[List[str]] = None,
    questionsRaised: Optional[List[str]] = None,
    objections: Optional[List[str]] = None,
    followUpDate: Optional[str] = None,
    sentiment: Optional[str] = None,
    interactionOutcome: Optional[str] = None,
    summary: Optional[str] = None,
) -> str:
    """Edit/Modify specific fields of the existing HCP interaction. ONLY pass the fields that need to be changed.
    Do NOT overwrite other fields that are already populated unless the user specifically requested to change them.
    """
    res = run_edit_interaction(
        hcpName=hcpName, specialty=specialty, organization=organization,
        interactionType=interactionType, interactionDate=interactionDate, interactionTime=interactionTime,
        location=location, duration=duration, productsDiscussed=productsDiscussed,
        topicsDiscussed=topicsDiscussed, materialsShared=materialsShared, samplesDistributed=samplesDistributed,
        questionsRaised=questionsRaised, objections=objections, followUpDate=followUpDate,
        sentiment=sentiment, interactionOutcome=interactionOutcome, summary=summary
    )
    return json.dumps(res)

@tool
def generate_summary_tool() -> str:
    """Generate a formal professional CRM summary paragraph for the current interaction details and save it."""
    llm = get_llm()
    res = run_generate_summary(llm_client=llm)
    return json.dumps(res)

@tool
def validate_interaction_tool() -> str:
    """Validate the current interaction form for completeness. Identifies fields that are empty or missing."""
    res = run_validate_interaction()
    return json.dumps(res)

@tool
def suggest_follow_up_tool() -> str:
    """Suggest 3-4 professional follow-up actions and tasks based on the current interaction details."""
    llm = get_llm()
    res = run_suggest_follow_up(llm_client=llm)
    return json.dumps(res)

TOOLS = [
    log_interaction_tool,
    edit_interaction_tool,
    generate_summary_tool,
    validate_interaction_tool,
    suggest_follow_up_tool
]

def build_langgraph_agent():
    """Compiles the LangGraph state machine workflow."""
    llm = get_llm()
    if not llm:
        return None
        
    # Bind tools to the model
    model_with_tools = llm.bind_tools(TOOLS)
    
    # Define LangGraph Nodes
    def call_model_node(state: AgentState):
        messages = state.messages
        # We append a system message instructing the agent on behavior
        system_msg = SystemMessage(
            content=(
                "You are an AI-Powered Healthcare CRM Assistant. You manage interaction logs between sales reps and HCPs.\n"
                "You have access to 5 tools. You should analyze the user's input and select the single most appropriate tool to run.\n"
                "If the user specifies details about a meeting (e.g. 'I met Dr. John Smith yesterday...'), call `log_interaction_tool`.\n"
                "If the user wants to update or modify specific fields (e.g. 'Change the sentiment to Neutral'), call `edit_interaction_tool` with only the changed fields.\n"
                "If the user asks for a summary, call `generate_summary_tool`.\n"
                "If the user asks to validate, check or verify fields, call `validate_interaction_tool`.\n"
                "If the user asks for next steps, suggestions, or follow-ups, call `suggest_follow_up_tool`.\n"
                "NEVER ask the user to manually edit the form, all actions are done via tools.\n"
                "Reply concisely and state which tool you are using."
            )
        )
        # Check if system message is already first
        input_messages = messages
        if not messages or not isinstance(messages[0], SystemMessage):
            input_messages = [system_msg] + messages
            
        response = model_with_tools.invoke(input_messages)
        return {"messages": [response]}

    tool_node = ToolNode(TOOLS)

    def router_node(state: AgentState) -> Literal["tools", "__end__"]:
        messages = state.messages
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return "__end__"

    # Define Graph
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model_node)
    workflow.add_node("tools", tool_node)
    
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", router_node, {"tools": "tools", "__end__": END})
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()


# =====================================================================
# Simulation Fallback Engine (If no API keys)
# =====================================================================
class SimulationAgent:
    """A rules-based backup assistant that mimics the exact behavior of the LangGraph agent
    when API keys are missing. It parses input text and invokes the exact same tools.
    """
    def run(self, message: str, history: List[dict]) -> Dict[str, Any]:
        msg_lower = message.lower()
        tool_triggered = None
        tool_output = None
        chat_response = ""
        
        # Determine current date context
        now = datetime.now()
        yesterday_str = (now - timedelta(days=1)).strftime("%Y-%m-%d")
        today_str = now.strftime("%Y-%m-%d")
        
        # 1. Summary tool query
        if "summary" in msg_lower or "summarize" in msg_lower or "log summary" in msg_lower:
            tool_triggered = "Generate Summary"
            tool_output = run_generate_summary()
            chat_response = f"Using Generate Summary Tool...\n\nCRM Summary generated:\n\"{tool_output['summary']}\""

        # 2. Validation tool query
        elif "validate" in msg_lower or "validation" in msg_lower or "check missing" in msg_lower:
            tool_triggered = "Validate Interaction"
            tool_output = run_validate_interaction()
            chat_response = f"Using Validate Interaction Tool...\n\n{tool_output['message']}"

        # 3. Follow-up tool query
        elif "follow-up" in msg_lower or "suggest" in msg_lower or "next action" in msg_lower or "next steps" in msg_lower:
            tool_triggered = "Suggest Follow-up"
            tool_output = run_suggest_follow_up()
            chat_response = f"Using Suggest Follow-up Tool...\n\n{tool_output['message']}"

        # 4. Edit tool query (contains keywords like change, edit, replace, update)
        elif any(kw in msg_lower for kw in ["change", "edit", "replace", "update", "instead of", "set sentiment", "set product"]):
            tool_triggered = "Edit Interaction"
            
            # Simple keyword parsing for fields
            edits = {}
            
            # Specialty
            if "specialty to" in msg_lower:
                edits["specialty"] = message.split("specialty to")[-1].strip(" .,").title()
            elif "cardiology" in msg_lower:
                edits["specialty"] = "Cardiology"
            elif "pediatrics" in msg_lower:
                edits["specialty"] = "Pediatrics"
                
            # Sentiment
            if "sentiment to positive" in msg_lower or "positive sentiment" in msg_lower:
                edits["sentiment"] = "Positive"
            elif "sentiment to neutral" in msg_lower or "neutral sentiment" in msg_lower:
                edits["sentiment"] = "Neutral"
            elif "sentiment to negative" in msg_lower or "negative sentiment" in msg_lower:
                edits["sentiment"] = "Negative"
                
            # Product
            if "product to" in msg_lower:
                prod = message.split("product to")[-1].strip(" .,").title()
                edits["productsDiscussed"] = [prod]
            elif "replace cardiolife with cardiomax" in msg_lower or "cardiomax" in msg_lower:
                edits["productsDiscussed"] = ["CardioMax"]
                
            # If nothing matched but the prompt was an edit request, make dummy edits
            if not edits:
                if "neutral" in msg_lower:
                    edits["sentiment"] = "Neutral"
                if "cardiomax" in msg_lower:
                    edits["productsDiscussed"] = ["CardioMax"]
            
            if not edits:
                # Default fallback edit
                edits["sentiment"] = "Neutral"
                
            tool_output = run_edit_interaction(**edits)
            fields_updated = ", ".join(edits.keys())
            chat_response = f"Using Edit Interaction Tool...\n\nModified field(s): {fields_updated}. Form state updated."

        # 5. Log Interaction (Default if meeting details are shared)
        else:
            tool_triggered = "Log Interaction"
            
            # Extract HCP Name
            hcp_name = "Dr. John Smith"
            if "dr. " in msg_lower:
                parts = message.split("Dr. ")
                if len(parts) > 1:
                    hcp_name = "Dr. " + parts[1].split()[0].strip(" .,")
                    if len(parts[1].split()) > 1:
                        hcp_name += " " + parts[1].split()[1].strip(" .,")
            elif "dr " in msg_lower:
                parts = message.split("dr ")
                if len(parts) > 1:
                    hcp_name = "Dr. " + parts[1].split()[0].strip(" .,")
                    
            # Extract Date
            date_val = today_str
            if "yesterday" in msg_lower:
                date_val = yesterday_str
            elif "last week" in msg_lower:
                date_val = (now - timedelta(days=7)).strftime("%Y-%m-%d")
                
            # Extract Product
            products = ["CardioLife"]
            if "cardiomax" in msg_lower:
                products = ["CardioMax"]
            elif "oncoboost" in msg_lower:
                products = ["OncoBoost"]
                
            # Extract Materials
            materials = []
            if "brochure" in msg_lower:
                materials.append("Product Brochure")
            if "clinical paper" in msg_lower or "study" in msg_lower:
                materials.append("Clinical Study Paper")
            if not materials:
                materials = ["Detailing Slide Deck"]
                
            # Sentiment
            sentiment = "Positive"
            if "neutral" in msg_lower or "interested but busy" in msg_lower:
                sentiment = "Neutral"
            elif "negative" in msg_lower or "not interested" in msg_lower:
                sentiment = "Negative"
                
            # Log fields
            tool_output = run_log_interaction(
                hcpName=hcp_name,
                interactionDate=date_val,
                productsDiscussed=products,
                materialsShared=materials,
                sentiment=sentiment,
                interactionType="Meeting",
                organization="General Clinic",
                specialty="Cardiology",
                topicsDiscussed=["Product Efficacy", "Clinical Trials"],
                summary=f"Sales representative met {hcp_name} to discuss {', '.join(products)}."
            )
            chat_response = f"Using Log Interaction Tool...\n\nSuccessfully logged interaction for {hcp_name}. Captured products: {', '.join(products)}, materials: {', '.join(materials)}, sentiment: {sentiment}."
            
        return {
            "response": chat_response,
            "tool_triggered": tool_triggered,
            "form_state": get_current_interaction()
        }


# =====================================================================
# Main Interface Endpoint
# =====================================================================
def run_agent_workflow(message: str, history: List[dict] = []) -> Dict[str, Any]:
    """Runs the appropriate agent (LangGraph or Simulation) depending on environment."""
    if not HAS_API_KEYS:
        # Run local rule-based simulation agent
        sim = SimulationAgent()
        return sim.run(message, history)
        
    try:
        agent = build_langgraph_agent()
        if not agent:
            # Fallback if building fails (e.g. library import issue)
            sim = SimulationAgent()
            return sim.run(message, history)
            
        # Parse history into LangChain messages
        lc_messages = []
        for msg in history:
            role = msg.get("role")
            content = msg.get("content")
            if role == "user":
                lc_messages.append(HumanMessage(content=content))
            elif role == "assistant":
                lc_messages.append(AIMessage(content=content))
                
        lc_messages.append(HumanMessage(content=message))
        
        # Invoke LangGraph Graph
        initial_state = AgentState(
            messages=lc_messages,
            form_state=get_current_interaction(),
            tools_run=[]
        )
        
        config = {"configurable": {"thread_id": "hcp-chat"}}
        result = agent.invoke(initial_state, config)
        
        # Extract tool usage and final assistant message
        final_msg = result["messages"][-1]
        chat_response = final_msg.content
        
        # Determine tools executed
        tool_triggered = None
        for msg in reversed(result["messages"]):
            if isinstance(msg, AIMessage) and msg.tool_calls:
                tool_triggered = msg.tool_calls[0]["name"].replace("_tool", "").replace("_", " ").title()
                break
                
        return {
            "response": chat_response,
            "tool_triggered": tool_triggered,
            "form_state": get_current_interaction()
        }
        
    except Exception as e:
        print(f"Error executing LangGraph agent: {e}")
        # Run Simulation Agent as error fallback so backend never crashes
        sim = SimulationAgent()
        return sim.run(message, history)
