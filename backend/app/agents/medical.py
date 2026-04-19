from ..tools import search_pubmed

def medical_researcher_node(state, llm):
    print(f"--- MEDICAL RESEARCHER: Analyzing {state['drug_name']} ---")
    raw_results = search_pubmed.invoke(state['drug_name'])
    
    prompt = (
        f"You are a Clinical Data Analyst. Review these PubMed results for {state['drug_name']}: {raw_results}.\n"
        "Provide a concise technical summary. Use bullet points for:\n"
        "- Biological Mechanism\n"
        "- Potential New Indications\n"
        "- Key Study Findings\n"
        "Avoid conversational filler. Professional tone only."
    )
    ai_msg = llm.invoke(prompt)
    return {"research_notes": [f"MEDICAL_INSIGHT: {ai_msg.content}"]}