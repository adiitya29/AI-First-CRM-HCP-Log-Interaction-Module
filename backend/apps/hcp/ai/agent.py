"""
LangGraph AI Agent for parsing natural language interactions.
Uses Groq's llama-3.3-70b-versatile via LangChain's ChatGroq.
"""
from typing import Annotated, TypedDict
from django.conf import settings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END

from .schemas import InteractionExtraction


# ─── State Definition ─────────────────────────────────────────────────────────

class AgentState(TypedDict):
    """The state of the interaction parsing graph."""
    user_message: str
    parsed_data: InteractionExtraction | None
    error: str | None


# ─── Nodes ────────────────────────────────────────────────────────────────────

def parse_interaction_node(state: AgentState) -> AgentState:
    """
    Node that calls the Groq LLM to extract structured data from the user's message.
    """
    user_message = state["user_message"]
    
    # Initialize the LLM using settings
    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name=settings.GROQ_MODEL,
        temperature=0.0, # low temp for reliable extraction
    )
    
    # Use LangChain's with_structured_output for robust extraction
    structured_llm = llm.with_structured_output(InteractionExtraction)
    
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an AI assistant for pharmaceutical and life-science field representatives. "
            "Your job is to parse natural language interaction notes and extract ONLY the fields "
            "that are explicitly mentioned in the message into a CRM structure.\n\n"
            "CRITICAL RULE: Set a field to null if the user did NOT explicitly mention it. "
            "Never infer or assume values. Only populate what the user actually said.\n\n"
            "FIELD RULES:\n"
            "1. HCP NAME: Extract if a doctor/HCP name is mentioned. Null otherwise.\n"
            "2. INTERACTION TYPE: One of 'in_person', 'phone', 'email', 'virtual', 'event'. "
            "Null if the user did NOT explicitly state how the meeting happened.\n"
            "3. DATE: YYYY-MM-DD format. Null if not mentioned.\n"
            "4. TIME: HH:MM 24-hour format (e.g. '3pm'→'15:00'). Null if not mentioned.\n"
            "5. ATTENDEES: Names of people present at the meeting (NOT the HCP). Null if not mentioned.\n"
            "6. NOTES: ONLY discussion topics, talking points, clinical data, HCP observations. "
            "Do NOT include attendees, outcomes, samples, or follow-up. Null if not mentioned.\n"
            "7. OUTCOMES: Key agreements or results reached (e.g. 'HCP agreed to prescribe'). "
            "Do NOT put samples/materials here. Null if not mentioned.\n"
            "8. PRODUCTS DISCUSSED: Drugs/devices/products discussed by name. Null if not mentioned.\n"
            "9. SAMPLES DISTRIBUTED: Physical product samples or materials GIVEN to the HCP. "
            "Null if the user did not mention distributing samples or materials.\n"
            "10. FOLLOW-UP: follow_up_required=true only if rep explicitly mentions a next meeting. "
            "Null if not mentioned.\n"
            "11. SENTIMENT: 'positive' (receptive/enthusiastic), 'negative' (dismissive/skeptical), "
            "or 'neutral'. Null if the user did NOT mention or imply the HCP's mood.\n"
            "12. AI SUMMARY: Always generate a concise 1-2 sentence summary of what was said."
        ),
        ("human", "{message}")
    ])
    
    # Chain: Prompt -> LLM (Structured)
    chain = prompt | structured_llm
    
    try:
        parsed_data = chain.invoke({"message": user_message})
        return {"parsed_data": parsed_data, "error": None}
    except Exception as e:
        return {"parsed_data": None, "error": str(e)}


# ─── Graph Construction ───────────────────────────────────────────────────────

# Initialize the StateGraph
workflow = StateGraph(AgentState)

# Add the parsing node
workflow.add_node("parse", parse_interaction_node)

# Define edges
workflow.add_edge(START, "parse")
workflow.add_edge("parse", END)

# Compile the graph
agent = workflow.compile()

def parse_interaction_text(message: str) -> dict:
    """
    Helper function to invoke the graph synchronously and return the parsed dict or an error.
    """
    initial_state = {"user_message": message, "parsed_data": None, "error": None}
    
    result = agent.invoke(initial_state)
    
    if result.get("error"):
        return {"error": result["error"]}
    
    if result.get("parsed_data"):
        return result["parsed_data"].model_dump()
        
    return {"error": "Failed to extract data."}
