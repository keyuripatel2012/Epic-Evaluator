import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def call_llm_with_prompt(prompt_file: str, variables: dict):
    
    with open(f"prompts/{prompt_file}") as f:
        template = f.read()

    prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", "{epic_text}") if "epic_text" in variables else ("human", "{element_name}: {element_content}")
    ])
    return (prompt | llm).invoke(variables).content
