def aggregate_evaluations(evaluations: dict) -> dict:
    assessments = []
    for element, result in evaluations.items():
        assessments.append({
            "element": element,
            "quality": result.get("quality", "Element Not Found"),
            "explanation": result.get("explanation", "Not provided."),
            "recommendations": result.get("recommendations", "No suggestions.")
        })
    return {"assessments": assessments}
