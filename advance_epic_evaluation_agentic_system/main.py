import streamlit as st
from graph import compiled_workflow
from models import EpicEvaluationState

st.set_page_config(page_title="Epic Evaluator", layout="wide")
st.title("Epic Evaluator")

epic_text = st.text_area("Paste Epic Text", height=200)

if st.button("Evaluate Epic"):
    if not epic_text.strip():
        st.warning("Please paste an epic to evaluate.")
    else:
        with st.spinner("Running evaluation..."):

            initial_state = EpicEvaluationState(
                epic_text=epic_text,
                retry_count=0,
                next_node="evaluate_title",
            )

            step_count = 1
            for step in compiled_workflow.stream(initial_state):
                for node_name, output in step.items():
                    with st.expander(f"🔹 Step {step_count}: {node_name}", expanded=True):
                        st.markdown(f"**Node:** `{node_name}`")
                        st.json(output)
                    step_count += 1

        st.success("Evaluation completed.")
