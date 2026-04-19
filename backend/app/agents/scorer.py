def strategic_scorer_node(state, llm):
    print(f"--- STRATEGIC SCORER: Finalizing Dossier for {state['drug_name']} ---")
    context = "\n\n".join(state["research_notes"])
    
    prompt = (
        f"Review this dossier for {state['drug_name']}:\n\n{context}\n\n"
        "Generate a final executive summary. You MUST include a 'Metrics' section at the end. "
        "Calculate the following based on the complexity of the research:\n"
        "1. Time Saved (e.g., 8 weeks to <1 week)\n"
        "2. Cost Savings (e.g., $15k to <$1k)\n"
        "3. Research Hours Reduction (e.g., 250 hours to 25 hours)\n"
        "\nFinish with this EXACT JSON block for the UI:\n"
        "```json\n"
        "{"
        "  \"impact_score\": 0-100,"
        "  \"metrics\": {"
        "    \"time_manual\": \"2-3 months\", \"time_ai\": \"<1 week\", \"time_impact\": \"8-12x faster\","
        "    \"cost_manual\": \"$10k-15k\", \"cost_ai\": \"<$1k\", \"cost_impact\": \"85-90% saving\","
        "    \"hours_manual\": \"200-300\", \"hours_ai\": \"20-30\", \"hours_impact\": \"~90% reduction\""
        "  },"
        "  \"verdict\": \"Go/No-Go\""
        "}\n"
        "```"
    )
    ai_msg = llm.invoke(prompt)
    return {"research_notes": [f"FINAL_VERDICT: {ai_msg.content}"]}