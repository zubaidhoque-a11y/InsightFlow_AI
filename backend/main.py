
import os
from typing_extensions import TypedDict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

from backend.data_analyzer import analyze_csv
from backend.chart_generator import generate_charts

load_dotenv()


# Initialize the Groq LLM
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
)


# Define the shared workflow state
class InsightFlowState(TypedDict):
    question: str
    answer: str
    csv_path: str
    chart_paths: list[str]


# AI agent for general questions
def ai_agent(state: InsightFlowState):
    response = llm.invoke(state["question"])
    return {"answer": response.content}


# Agent for analyzing the uploaded CSV
def csv_agent(state: InsightFlowState):
    answer = analyze_csv(
        state["csv_path"],
        state["question"],
        llm,
    )
    return {"answer": answer}


# Choose the appropriate agent
def route_question(state: InsightFlowState):
    if state.get("csv_path", "").strip():
        return "csv_agent"

    return "ai_agent"


# Agent that generates actual chart image files
def chart_agent(state: InsightFlowState):
    csv_path = state["csv_path"]

    generated_paths = generate_charts(csv_path) or []

    # Keep only valid PNG files
    valid_paths = [
        os.path.abspath(path)
        for path in generated_paths
        if isinstance(path, str)
        and path.lower().endswith(".png")
        and os.path.isfile(path)
    ]

    print("Generated chart paths:", valid_paths)

    # IMPORTANT: The key must be chart_paths, not chart_path
    return {"chart_paths": valid_paths}


# Build the LangGraph workflow
graph = StateGraph(InsightFlowState)

graph.add_node("ai_agent", ai_agent)
graph.add_node("csv_agent", csv_agent)
graph.add_node("chart_agent", chart_agent)

graph.add_conditional_edges(
    START,
    route_question,
    {
        "ai_agent": "ai_agent",
        "csv_agent": "csv_agent",
    },
)

graph.add_edge("ai_agent", END)
graph.add_edge("csv_agent", "chart_agent")
graph.add_edge("chart_agent", END)

workflow = graph.compile()


# Run directly from the terminal when needed
if __name__ == "__main__":
    question = input("Ask InsightFlow AI: ")
    csv_path = input("Enter CSV path (or press Enter to skip): ")

    result = workflow.invoke({
        "question": question,
        "answer": "",
        "csv_path": csv_path,
        "chart_paths": [],
    })

    print("\nInsightFlow AI:", result.get("answer", ""))

    print("\nGenerated charts:")
    for path in result.get("chart_paths", []):
        print(path)
