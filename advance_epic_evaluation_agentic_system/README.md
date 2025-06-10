# Epic Evaluator: LangGraph Multi-Agent System

## Features:
- Parses Agile Epic into parts
- Evaluates each part using LLM
- Routes LOW-quality parts to refinement
- Final output is structured JSON report

## Tech:
- LangGraph
- Google Gemini 2.0
- Pydantic state

## How to Run:
```bash
pip install -r requirements.txt
python main.py


# Epic Evaluator: Multi-Agent LangGraph System

## Graph Nodes:
- `EpicParserNode`: Extracts key elements from raw epic text.
- `EvaluatorNode`: Evaluates each element (Title, Problem Statement, etc.).
- `RefinementNode`: Improves elements with LOW score.
- `AggregatorNode`: Generates final structured report.

## Conditional Flow:
- Elements scoring LOW are refined and re-evaluated (max 2 attempts).
- Parsed data, evaluations, and retry state managed with Pydantic models.

## How to Run:
```bash
python main.py
