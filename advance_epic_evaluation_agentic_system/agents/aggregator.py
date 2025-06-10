from models import EpicEvaluationState

def aggregate_report_node(state: EpicEvaluationState) -> EpicEvaluationState:
    parsed = state.elements or {}
    evaluations = state.evaluations or {}

    aggregated = {
        "parsed": parsed,
        "evaluations": {k: v.dict() for k, v in evaluations.items()}
    }

    state.aggregated_report = aggregated
    return state

def aggregate_results(state: EpicEvaluationState) -> dict:
    parsed = state.elements or {}
    evaluations = state.evaluations or {}

    return {
        "parsed": parsed,
        "evaluations": {k: v.dict() for k, v in evaluations.items()}
    }
