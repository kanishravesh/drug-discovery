from ..tools import search_patents 
def market_intelligence_node(state, llm):
    """
    Expert Agent: Assesses market size, unmet needs, and revenue potential.
    """
    print(f"--- MARKET INTELLIGENCE: Assessing commercial potential for {state['drug_name']} ---")
    
    try:
       
        query = f"{state['drug_name']} market size global prevalence unmet medical need revenue potential"
        market_data = search_patents.invoke(query)
        
        prompt = (
            f"You are a Pharmaceutical Market Analyst. Analyze this data for {state['drug_name']}:\n\n{market_data}\n\n"
            "Provide a concise commercial summary including:\n"
            "- Estimated Target Patient Population\n"
            "- Current Market Size and Growth (CAGR)\n"
            "- Primary Competitors and Unmet Needs\n"
            "Professional tone. No conversational filler."
        )
        ai_msg = llm.invoke(prompt)
        
        return {"research_notes": [f"MARKET_INSIGHT: {ai_msg.content}"]}
    
    except Exception as e:
        return {"research_notes": [f"MARKET_ERROR: {str(e)}"]}