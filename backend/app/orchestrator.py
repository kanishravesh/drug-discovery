import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from .agents.medical import medical_researcher_node
from .agents.patent import patent_analyst_node
from .agents.market import market_intelligence_node
from .agents.clinical import clinical_trials_node
from .agents.scorer import strategic_scorer_node
from .state import AgentState

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)

builder = StateGraph(AgentState)

builder.add_node("medical_researcher", lambda state: medical_researcher_node(state, llm))
builder.add_node("patent_analyst", lambda state: patent_analyst_node(state, llm))
builder.add_node("market_intelligence", lambda state: market_intelligence_node(state, llm))
builder.add_node("clinical_trials", lambda state: clinical_trials_node(state, llm))
builder.add_node("strategic_scorer", lambda state: strategic_scorer_node(state, llm))

builder.add_edge(START, "medical_researcher")
builder.add_edge("medical_researcher", "patent_analyst")
builder.add_edge("patent_analyst", "market_intelligence") 
builder.add_edge("market_intelligence", "clinical_trials") 
builder.add_edge("clinical_trials", "strategic_scorer")
builder.add_edge("strategic_scorer", END)

graph = builder.compile()