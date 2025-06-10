from models import EpicEvaluationState

def evaluation_router_node(state: EpicEvaluationState) -> EpicEvaluationState:
    evaluation_order = [
        "evaluate_title",
        "evaluate_problem_statement",
        "evaluate_product_outcome_and_instrumentation",
        "evaluate_user_stories",
        "evaluate_non_functional_requirements",
        "aggregate_report"
    ]

    label_mapping = {
        "evaluate_title": "Title",
        "evaluate_problem_statement": "Problem Statement",
        "evaluate_product_outcome_and_instrumentation": "Product Outcome & Instrumentation",
        "evaluate_user_stories": "User Stories",
        "evaluate_non_functional_requirements": "Non-Functional Requirements",
    }

    current_node = state.next_node or "evaluate_title"
    current_label = label_mapping.get(current_node, "Unknown")

    last_eval = state.evaluations.get(current_label)

    if (
        last_eval and 
        last_eval.quality and 
        last_eval.quality.lower() == "low"
    ):
        attempts = state.refinement_attempts.get(current_label, 0)
        if attempts < state.max_refinements:
            state.refinement_attempts[current_label] = attempts + 1
            state.next_node = "refine"
            return state

    try:
        current_index = evaluation_order.index(current_node)
        state.next_node = evaluation_order[current_index + 1]
    except (ValueError, IndexError):
        state.next_node = "aggregate_report"

    state.last_evaluated = label_mapping.get(state.next_node, "Unknown")
    return state
