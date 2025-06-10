# Epic Evaluation Agentic System

## Overview
Aa project ek multi-agent system che je Epic documents ne analyze kare che using LangGraph and Gemini LLMs. System structured parsing, conditional evaluation ane refinement logic vapre che.

## Technologies
- Python
- LangGraph
- Google Gemini (2.0 Flash)
- Pydantic

## Workflow
1. **Parsing** – Extracts elements (title, problem statement, etc.)
2. **Evaluation** – Each element evaluated for quality, explanation, recommendation
3. **Router** – Conditional logic to decide whether to continue, refine or stop
4. **Refinement** – Weak elements are improved (up to 2 times)
5. **Aggregation** – Generates a final JSON report

## Node Overview

| Node | Function |
|------|----------|
| `parse` | Parses epic into components |
| `evaluate_*` | Evaluates individual components |
| `router` | Decides next step based on evaluation |
| `refine` | Enhances weak parts (if needed) |
| `aggregate_report` | Final report compilation |

## How to Run

```bash
streamlit run main.py
