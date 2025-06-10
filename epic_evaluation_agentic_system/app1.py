import streamlit as st

from dotenv import load_dotenv
from utils.file_upload import extract_text_from_file
from agents.element_identifier import extract_elements
from agents.element_evaluator import evaluate_element
from agents.aggregator import aggregate_evaluations

load_dotenv()
st.title("Epic Evaluator: Agile Epic Quality Checker")

uploaded_file = st.file_uploader("Upload your Agile Epic file (txt, pdf, docx)", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    epic_text = extract_text_from_file(uploaded_file)
    if epic_text is None:
        st.error("Unsupported file format or failed to extract text.")
    else:
        st.text_area("Extracted Epic Text:", value=epic_text, height=300)

if st.button("Evaluate Epic"):
    if not epic_text or not epic_text.strip():
        st.warning("Please enter or upload an Agile Epic.")
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
