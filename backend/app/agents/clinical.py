from ..tools import search_patents 

def clinical_trials_node(state, llm):
    """
    Expert Agent: Evaluates trial outcomes and development feasibility.
    """
    print(f"--- CLINICAL TRIALS: Evaluating trial history for {state['drug_name']} ---")
    
    try:

        query = f"{state['drug_name']} clinical trials phases results success rate safety endpoints"
        trial_data = search_patents.invoke(query)
        
        prompt = (
            f"You are a Clinical Trials Coordinator. Analyze this data for {state['drug_name']}:\n\n{trial_data}\n\n"
            "Provide a clinical feasibility summary. Include:\n"
            "- Highest Clinical Phase Reached\n"
            "- Safety Profile Summary (Adverse Events)\n"
            "- Feasibility of new trials for repurposing\n"
            "Keep it concise and evidence-backed. No conversational filler."
        )
        ai_msg = llm.invoke(prompt)
        
        return {"research_notes": [f"CLINICAL_INSIGHT: {ai_msg.content}"]}
    
    except Exception as e:
        return {"research_notes": [f"CLINICAL_ERROR: {str(e)}"]}