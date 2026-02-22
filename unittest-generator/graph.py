from langgraph.graph import StateGraph, END
from state import TestGenerationState
from nodes import (
    load_modules,
    select_next_module,
    generate_test,
    run_test,
    should_retry,
    mark_completed,
    check_completion
)

def create_graph():
    """Create the LangGraph workflow."""
    workflow = StateGraph(TestGenerationState)
    
    # Add nodes
    workflow.add_node("load_modules", load_modules)
    workflow.add_node("select_next_module", select_next_module)
    workflow.add_node("generate_test", generate_test)
    workflow.add_node("run_test", run_test)
    workflow.add_node("mark_completed", mark_completed)
    
    # Set entry point
    workflow.set_entry_point("load_modules")
    
    # Add edges
    workflow.add_edge("load_modules", "select_next_module")
    
    workflow.add_conditional_edges(
        "select_next_module",
        lambda s: "done" if s["current_module"] is None else "generate",
        {
            "generate": "generate_test",
            "done": END
        }
    )
    
    workflow.add_edge("generate_test", "run_test")
    
    workflow.add_conditional_edges(
        "run_test",
        should_retry,
        {
            "retry": "generate_test",
            "skip": "mark_completed",
            "next": "select_next_module"
        }
    )
    
    workflow.add_edge("mark_completed", "select_next_module")
    
    return workflow.compile()
