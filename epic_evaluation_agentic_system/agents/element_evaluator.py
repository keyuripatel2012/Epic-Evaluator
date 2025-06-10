import os
import json
import regex as re

from dotenv import load_dotenv
from utils.clean_text import clean_text  
from utils.prompt_loader import load_prompt
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

prompt_template = load_prompt("evaluate_element.txt")
prompt = ChatPromptTemplate.from_messages([
    ("system", prompt_template),
    ("human", "{element_content}")
])

chain = prompt | llm

def evaluate_element(element_name, element_content):
    if not element_content or (isinstance(element_content, list) and len(element_content) == 0):
        return {
            "quality": "Element Not Found",
            "explanation": f"No content provided for '{element_name}'. This field is optional but valuable for clarity and completeness.",
            "recommendations": f"Consider including a well-defined '{element_name}' to enhance the quality of your Agile Epic."
        }

    response = chain.invoke({
        "element_name": element_name,
        "element_content": element_content
    })

    raw_text = response.content.strip()

    try:
        match = re.search(r"\{(?:[^{}]|(?R))*\}", raw_text, re.DOTALL)
        if match:
            result = json.loads(match.group())
            if "quality" in result:
                q = result["quality"].strip().capitalize()
                result["quality"] = q if q in ["High", "Medium", "Low"] else "Medium"
            if "explanation" in result:
                result["explanation"] = clean_text(result["explanation"])
            if "recommendations" in result:
                result["recommendations"] = clean_text(result["recommendations"])
            return result
        else:
            raise ValueError("No valid JSON found in evaluation response.")
    except Exception as e:
        return {
            "quality": "Element Not Found",
            "explanation": f"Evaluation failed for '{element_name}': {e}",
            "recommendations": f"Ensure '{element_name}' exists and is clearly described."
        }
