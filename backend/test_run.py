from app.orchestrator import graph

# user input
initial_input = {"drug_name": "Metformin"}

# Run the graph
final_state = graph.invoke(initial_input)

# results
print("\nFinal Research Notes:")
print(final_state["research_notes"])