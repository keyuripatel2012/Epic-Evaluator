from pydantic import BaseModel
from typing import Dict, List, Optional, Union

class ParsedEpic(BaseModel):
    title: Optional[str]
    problem_statement: Optional[str]
    outcome: Optional[str]
    user_stories: Optional[List[str]]
    non_functional_requirements: Optional[List[str]]

class Evaluation(BaseModel):
    score: Optional[int] = None
    feedback: Optional[str] = None
    quality: Optional[str] = None
    explanation: Optional[str] = None
    recommendations: Optional[str] = None

class EpicEvaluationState(BaseModel):
    epic_text: str
    elements: Dict[str, Union[str, List[str]]] = {}
    evaluations: Dict[str, Evaluation] = {}
    last_evaluated: Optional[str] = None
    refinement_attempts: Dict[str, int] = {}
    max_refinements: int = 2
    parsing_success: bool = False
    retry_count: int = 0
    next_node: Optional[str] = None
    aggregated_report: Optional[str] = None 