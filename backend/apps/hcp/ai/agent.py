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
            "Your job is to parse the natural language notes provided by a rep after a visit with a "
            "Healthcare Professional (HCP) and extract the structured data needed for the CRM.\n\n"
            "EXTRACTION RULES — follow these strictly:\n"
            "1. HCP NAME: Extract the doctor/HCP name if mentioned (e.g., 'Dr. Smith').\n"
            "2. INTERACTION TYPE: One of 'in_person', 'phone', 'email', 'virtual', 'event'. Default to 'in_person'.\n"
            "3. DATE: In YYYY-MM-DD format. Use null if not explicitly mentioned.\n"
            "4. TIME: In HH:MM 24-hour format (e.g., '3pm' → '15:00', '10:30am' → '10:30'). Use null if not mentioned.\n"
            "5. ATTENDEES: Any person names mentioned as present at the meeting (NOT the HCP themselves). Put them in the attendees list.\n"
            "6. NOTES: ONLY discussion topics, product information shared, HCP observations, and key talking points. "
            "Do NOT put attendees, outcomes, or follow-up info in notes.\n"
            "7. OUTCOMES: Key results, agreements, or commitments made during the interaction (e.g., 'HCP agreed to try the product', 'Rep will send PDF'). "
            "Leave empty string if no specific outcomes mentioned.\n"
            "8. PRODUCTS DISCUSSED: List of specific product/drug/device names mentioned.\n"
            "9. FOLLOW-UP: Set follow_up_required=true and extract follow_up_date if the rep mentions scheduling a next meeting.\n"
            "10. SENTIMENT: Must be EXACTLY 'positive', 'neutral', or 'negative'. "
            "Positive = HCP was receptive/enthusiastic. Negative = HCP was dismissive/skeptical. Default = 'neutral'.\n"
            "11. AI SUMMARY: A concise 1-2 sentence summary of the entire interaction."
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
