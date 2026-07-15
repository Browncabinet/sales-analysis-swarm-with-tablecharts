"""sales-analysis-swarm-with-tablecharts — entry point.

Wires a 3-node LangGraph pipeline:

    analyst → chart → report

Run:
    python main.py
"""
from __future__ import annotations

import csv
import os
import sys
from typing import Dict, List

from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph

from agents.analyst_agent import analyst_node
from agents.chart_agent import chart_node
from agents.report_agent import report_node
from agents.state import SwarmState
from agents.tablecharts_tool import TableChartsError

DATA_FILE = "data/sales.csv"


def load_rows(path: str) -> List[Dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_graph():
    graph = StateGraph(SwarmState)
    graph.add_node("analyst", analyst_node)
    graph.add_node("chart", chart_node)
    graph.add_node("report", report_node)

    graph.add_edge(START, "analyst")
    graph.add_edge("analyst", "chart")
    graph.add_edge("chart", "report")
    graph.add_edge("report", END)

    return graph.compile()


def main() -> int:
    load_dotenv()

    rows = load_rows(DATA_FILE)
    app = build_graph()

    try:
        final_state = app.invoke({"rows": rows})
    except TableChartsError as e:
        print(f"\n❌ TableCharts error: {e}", file=sys.stderr)
        return 1

    print("\n" + "=" * 60)
    print(final_state["summary"])
    print("=" * 60)
    print(f"Report:   {os.path.abspath(final_state['report_path'])}")
    print(f"Charts:   {len(final_state['charts'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())