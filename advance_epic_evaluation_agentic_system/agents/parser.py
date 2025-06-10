import os
import json
import regex as re
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from models import EpicEvaluationState
from utils.prompt_loader import load_prompt

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.3,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

prompt_template = load_prompt("extract_elements.txt")

prompt = ChatPromptTemplate.from_messages([
    ("system", prompt_template),
    ("human", "{epic_text}")
])

chain = prompt | llm

def epic_parser_node(state: EpicEvaluationState) -> EpicEvaluationState:
    response = chain.invoke({"epic_text": state.epic_text})
    raw_text = response.content.strip()

    try:
        match = re.search(r"\{(?:[^{}]|(?R))*\}", raw_text, re.DOTALL)
        if match:
            parsed = json.loads(match.group())

            keys = [
                "Title",
                "Problem Statement",
                "Product Outcome & Instrumentation",
                "User Stories",
                "Non-Functional Requirements"
            ]
            for key in keys:
                if key not in parsed:
                    parsed[key] = "" if key != "User Stories" else []

            state.elements = parsed
            state.last_evaluated = "Title"
            state.next_node = "evaluate_title"
        else:
            state.next_node = "evaluate_title"
            state.elements = {}
    except Exception as e:
        state.elements = {}
        state.next_node = "evaluate_title"

    return state
