from agents.evaluator import (
    evaluate_title_node,
    evaluate_problem_node,
    evaluate_outcome_node,
    evaluate_user_stories_node,
    evaluate_non_functional_reqs_node,
)
from agents.refiner import refinement_node
from agents.parser import epic_parser_node
from agents.router import evaluation_router_node
from agents.aggregator import aggregate_report_node

from models import EpicEvaluationState
from langgraph.graph import StateGraph, END

workflow = StateGraph(EpicEvaluationState)

workflow.add_node("parse", epic_parser_node)
workflow.add_node("evaluate_title", evaluate_title_node)
workflow.add_node("evaluate_problem_statement", evaluate_problem_node)
workflow.add_node("evaluate_product_outcome_and_instrumentation", evaluate_outcome_node)
workflow.add_node("evaluate_user_stories", evaluate_user_stories_node)
workflow.add_node("evaluate_non_functional_requirements", evaluate_non_functional_reqs_node)
workflow.add_node("aggregate_report", aggregate_report_node)
workflow.add_node("refine", refinement_node)

def safe_router(state: EpicEvaluationState):
    if state.retry_count >= 3:
        return "aggregate_report"
    
    if state.next_node == "refine":
        state.retry_count += 1

    return state.next_node or "aggregate_report"

workflow.add_node("router", evaluation_router_node)

workflow.set_entry_point("parse")

workflow.add_edge("parse", "evaluate_title")
workflow.add_edge("evaluate_title", "router")
workflow.add_edge("evaluate_problem_statement", "router")
workflow.add_edge("evaluate_product_outcome_and_instrumentation", "router")
workflow.add_edge("evaluate_user_stories", "router")
workflow.add_edge("refine", "router")
workflow.add_edge("evaluate_non_functional_requirements", "aggregate_report")
workflow.add_edge("aggregate_report", END)

workflow.add_conditional_edges(
    "router",
    lambda state: state.next_node,
    {
        "evaluate_title": "evaluate_title",
        "evaluate_problem_statement": "evaluate_problem_statement",
        "evaluate_product_outcome_and_instrumentation": "evaluate_product_outcome_and_instrumentation",
        "evaluate_user_stories": "evaluate_user_stories",
        "evaluate_non_functional_requirements": "evaluate_non_functional_requirements",
        "aggregate_report": "aggregate_report",
        "refine": "refine",
    }
)

compiled_workflow = workflow.compile()
