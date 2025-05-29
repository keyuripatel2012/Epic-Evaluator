import os
import json
import regex as re

from dotenv import load_dotenv
from utils.prompt_loader import load_prompt
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

prompt_template = load_prompt("extract_elements.txt")
prompt = ChatPromptTemplate.from_messages([
    ("system", prompt_template),
    ("human", "{epic_text}")
])

chain = prompt | llm

def extract_elements(epic_text):
    response = chain.invoke({"epic_text": epic_text})
    raw_text = response.content.strip()

    try:
        match = re.search(r"\{(?:[^{}]|(?R))*\}", raw_text, re.DOTALL)
        if match:
            parsed = json.loads(match.group())
            keys = ["Title", "Problem Statement", "Product Outcome & Instrumentation", "User Stories", "Non-Functional Requirements"]
            for key in keys:
                if key not in parsed:
                    parsed[key] = "" if key != "User Stories" else []
            return parsed
        else:
            return {"error": "No JSON object found in model response"}
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON in model response: {e}"}
