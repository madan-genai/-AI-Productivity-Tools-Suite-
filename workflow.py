from langgraph.graph import StateGraph, START, END
from summarization import AgentState, route, summarization_state
from translation import translation
from grammar_check import grammar_check_state
from image_describer import image_describer

# -------------------------
# Initialize Graph
# -------------------------
graph = StateGraph(AgentState)

# -------------------------
# Nodes
# -------------------------
graph.add_node("summarization_state", summarization_state)
graph.add_node("translation", translation)
graph.add_node("grammar_check_state", grammar_check_state)
graph.add_node("image_describer", image_describer)

# -------------------------
# Conditional Routing
# -------------------------
graph.add_conditional_edges(
    START,
    route,
    {
        "summarization_state": "summarization_state",
        "translation": "translation",
        "grammar_check_state": "grammar_check_state",
        "image_describer": "image_describer"
    }
)

# -------------------------
# Terminal Edges
# -------------------------
graph.add_edge("summarization_state", END)
graph.add_edge("translation", END)
graph.add_edge("grammar_check_state", END)
graph.add_edge("image_describer", END)

# -------------------------
# Compile App
# -------------------------
app = graph.compile()
