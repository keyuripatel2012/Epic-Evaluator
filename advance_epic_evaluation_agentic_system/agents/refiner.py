import os
import json
import regex as re
from dotenv import load_dotenv
from utils.clean_text import clean_text
from utils.prompt_loader import load_prompt
from models import EpicEvaluationState, Evaluation
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

prompt_template = load_prompt("refiner_prompt.txt")
prompt = ChatPromptTemplate.from_messages([
    ("system", prompt_template),
    ("human", "{element_name}\n\n{element_content}\n\nEvaluation:\n{evaluation}")
])
chain = prompt | llm

def refinement_node(state: EpicEvaluationState) -> EpicEvaluationState:
    element_name = state.last_evaluated
    content = state.elements.get(element_name, "")
    evaluation = state.evaluations.get(element_name)

    response = chain.invoke({
        "element_name": element_name,
        "element_content": content,
        "evaluation": json.dumps(evaluation.dict() if evaluation else {}),
        "explanation": evaluation.explanation if evaluation else "",
        "quality": evaluation.quality if evaluation else ""
    })


    raw_text = response.content.strip()
    try:
        match = re.search(r"\{(?:[^{}]|(?R))*\}", raw_text, re.DOTALL)
        if match:
            refined_eval = json.loads(match.group())
            refined_eval["quality"] = refined_eval.get("quality", "Medium").capitalize()
            refined_eval["explanation"] = clean_text(refined_eval.get("explanation", ""))
            refined_eval["recommendations"] = clean_text(refined_eval.get("recommendations", ""))
            state.evaluations[element_name] = Evaluation(**refined_eval)
    except Exception as e:
        state.evaluations[element_name] = Evaluation(
            quality="Medium",
            explanation=f"Refinement failed: {e}",
            recommendations="Try rewriting or simplifying the content."
        )

    return state
