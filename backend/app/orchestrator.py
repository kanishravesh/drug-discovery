import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from .state import AgentState
from .tools import search_pubmed, search_patents

# 1. Load keys
load_dotenv()

# 2. Initialize Gemini 2.5 Flash
# This model is superior for the agentic reasoning required by your blueprint
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.1,
    request_timeout=60 # Research tasks can take a bit longer
)

# --- NODE 1: Medical Researcher (Literature Agent) ---
def medical_researcher(state: AgentState):
    print(f"--- MEDICAL RESEARCHER: Analyzing {state['drug_name']} ---")
    try:
        # Fetching real data from PubMed
        raw_results = search_pubmed.invoke(state['drug_name'])
        
        prompt = (
            f"As a medical researcher, analyze these findings for {state['drug_name']}: {raw_results}. "
            f"Explain why this drug is a strong candidate for repurposing."
        )
        ai_msg = llm.invoke(prompt)
        return {"research_notes": [f"MEDICAL_INSIGHT: {ai_msg.content}"]}
    except Exception as e:
        return {"research_notes": [f"MEDICAL_ERROR: {str(e)}"]}

# --- NODE 2: Patent Analyst (Legal Agent) ---
def patent_analyst(state: AgentState):
    print(f"--- PATENT ANALYST: Checking legal status for {state['drug_name']} ---")
    try:
        # Fetching real patent and legal data via Tavily
        patent_results = search_patents.invoke(state['drug_name'])
        
        prompt = (
            f"Analyze the following patent data for {state['drug_name']}: {patent_results}. "
            f"Determine if there is 'Freedom to Operate' for new medical uses. "
            f"Highlight potential legal barriers or patent expirations."
        )
        ai_msg = llm.invoke(prompt)
        return {"research_notes": [f"PATENT_INSIGHT: {ai_msg.content}"]}
    except Exception as e:
        return {"research_notes": [f"PATENT_ERROR: {str(e)}"]}

# --- GRAPH CONSTRUCTION ---
builder = StateGraph(AgentState)

# Add our specialized agents
builder.add_node("medical_researcher", medical_researcher)
builder.add_node("patent_analyst", patent_analyst)

# Sequence: Start -> Literature Research -> Legal Check -> End
builder.add_edge(START, "medical_researcher")
builder.add_edge("medical_researcher", "patent_analyst")
builder.add_edge("patent_analyst", END)

# Export the executable graph
graph = builder.compile()