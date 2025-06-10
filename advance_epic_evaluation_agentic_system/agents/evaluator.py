import os
import json
import regex as re
from dotenv import load_dotenv

from models import Evaluation
from models import EpicEvaluationState
from utils.clean_text import clean_text
from utils.prompt_loader import load_prompt

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

prompt_template = load_prompt("evaluate_element.txt")
prompt = ChatPromptTemplate.from_messages([
    ("system", prompt_template),
    ("human", "{element_name}: {element_content}")
])
chain = prompt | llm

def evaluate_element(name: str, content: str) -> dict:
    if not content or (isinstance(content, list) and not content):
        return {
            "quality": "Element Not Found",
            "explanation": f"No content provided for '{name}'.",
            "recommendations": f"Consider adding a well-defined '{name}'.",
            "score": 0,
            "feedback": f"'{name}' not found in the epic. Needs to be defined clearly."
        }

    response = chain.invoke({
        "element_name": name,
        "element_content": content
    })

    raw = response.content.strip()
    try:
        match = re.search(r"\{(?:[^{}]|(?R))*\}", raw, re.DOTALL)
        if match:
            result = json.loads(match.group())

            # Normalize and clean
            result["quality"] = result.get("quality", "Medium").capitalize()
            result["explanation"] = clean_text(result.get("explanation", ""))
            result["recommendations"] = clean_text(result.get("recommendations", ""))

            # ✅ Add score and feedback
            score_mapping = {"High": 3, "Medium": 2, "Low": 1}
            result["score"] = score_mapping.get(result["quality"], 2)
            result["feedback"] = f"Element rated as {result['quality']} based on provided content."

            return result
        else:
            raise ValueError("No valid JSON found.")
    except Exception as e:
        return {
            "quality": "Element Not Found",
            "explanation": f"Evaluation failed: {e}",
            "recommendations": "Try simplifying or rewording the content.",
            "score": 0,
            "feedback": f"Evaluation of '{name}' failed due to an error."
        }


def evaluate_title_node(state: EpicEvaluationState) -> EpicEvaluationState:
    content = state.elements.get("Title") if state.elements else None

    if not content:
        state.evaluations["Title"] = Evaluation(
            score=0,
            feedback="Element Not Found: The text does not contain a well-defined 'Title'.",
            quality="Element Not Found",
            explanation="No title was found in the input.",
            recommendations="Add a clear and descriptive Title."
        )
    else:
        eval_result = evaluate_element("Title", content)
        state.evaluations["Title"] = Evaluation(**eval_result)

    state.last_evaluated = "Title"
    return state

def evaluate_problem_node(state: EpicEvaluationState) -> EpicEvaluationState:
    content = state.elements.get("Problem Statement", "")
    state.last_evaluated = "Problem Statement"
    eval_result = evaluate_element("Problem Statement", content)
    state.evaluations["Problem Statement"] = Evaluation(**eval_result)
    return state

def evaluate_outcome_node(state: EpicEvaluationState) -> EpicEvaluationState:
    content = state.elements.get("Product Outcome & Instrumentation", "")
    state.last_evaluated = "Product Outcome & Instrumentation"
    eval_result = evaluate_element("Product Outcome & Instrumentation", content)
    state.evaluations["Product Outcome & Instrumentation"] = Evaluation(**eval_result)
    return state

def evaluate_user_stories_node(state: EpicEvaluationState) -> EpicEvaluationState:
    content = state.elements.get("User Stories", [])
    text = "\n".join(content) if isinstance(content, list) else str(content)
    state.last_evaluated = "User Stories"
    eval_result = evaluate_element("User Stories", text)
    state.evaluations["User Stories"] = Evaluation(**eval_result)
    return state

def evaluate_non_functional_reqs_node(state: EpicEvaluationState) -> EpicEvaluationState:
    content = state.elements.get("Non-Functional Requirements", "")
    state.last_evaluated = "Non-Functional Requirements"
    eval_result = evaluate_element("Non-Functional Requirements", content)
    state.evaluations["Non-Functional Requirements"] = Evaluation(**eval_result)
    return state