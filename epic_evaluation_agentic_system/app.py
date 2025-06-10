import streamlit as st

from dotenv import load_dotenv
from agents.element_identifier import extract_elements
from agents.element_evaluator import evaluate_element
from agents.aggregator import aggregate_evaluations

load_dotenv()
st.title("Epic Evaluator: Agile Epic Quality Checker")

epic_text = st.text_area("Paste your Agile Epic text here:", height=300)

if st.button("Evaluate Epic"):
    if not epic_text.strip():
        st.warning("Please enter an Agile Epic.")
    else:
        with st.spinner("Extracting elements..."):
            elements = extract_elements(epic_text)

        if "error" in elements:
            st.error(f"Extraction failed: {elements['error']}")
        else:
            evaluations = {}
            for name, content in elements.items():
                with st.spinner(f"Evaluating {name}..."):
                    result = evaluate_element(name, content)
                    if "quality" in result:
                        result["quality"] = result["quality"].capitalize()
                    evaluations[name] = result

            st.subheader("Evaluation Results")
            st.json(aggregate_evaluations(evaluations))
