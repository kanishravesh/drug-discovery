from ..tools import search_patents

def patent_analyst_node(state, llm):
    print(f"--- PATENT ANALYST: Checking legal status for {state['drug_name']} ---")
    patent_data = search_patents.invoke(state['drug_name'])
    
    prompt = (
        f"You are a Patent Attorney. Analyze this data for {state['drug_name']}: {patent_data}.\n"
        "Provide a structured legal summary. List:\n"
        "- Core Patent Expiration Date\n"
        "- Specific Combination/Method Blockers (if any)\n"
        "- Freedom to Operate (FTO) Status (High/Medium/Low)\n"
        "No introductory text. Get straight to the legal facts."
    )
    ai_msg = llm.invoke(prompt)
    return {"research_notes": [f"PATENT_INSIGHT: {ai_msg.content}"]}