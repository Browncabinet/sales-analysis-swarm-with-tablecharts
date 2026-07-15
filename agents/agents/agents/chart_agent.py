"""Chart agent — asks TableCharts to render 3 dashboards from the sales data."""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, List

from .state import ChartResult, SwarmState
from .tablecharts_tool import generate_dashboard


def _aggregate(rows: List[Dict], key: str) -> List[Dict]:
    agg: Dict[str, float] = defaultdict(float)
    for r in rows:
        agg[r[key]] += float(r["revenue"])
    # sort by revenue desc for a cleaner chart
    return [{key: k, "revenue": v} for k, v in sorted(agg.items(), key=lambda x: -x[1])]


def chart_node(state: SwarmState) -> SwarmState:
    rows = state["rows"]
    charts: List[ChartResult] = []

    # Chart 1: revenue by month (line chart auto-picked)
    monthly = sorted(_aggregate(rows, "month"), key=lambda x: x["month"])
    charts.append(
        _make_chart("revenue_by_month", "Revenue by Month", monthly, chart_type="line")
    )

    # Chart 2: revenue by region (bar chart)
    charts.append(
        _make_chart(
            "revenue_by_region", "Revenue by Region", _aggregate(rows, "region"), chart_type="bar"
        )
    )

    # Chart 3: top products (bar chart)
    charts.append(
        _make_chart(
            "top_products", "Top Products by Revenue", _aggregate(rows, "product"), chart_type="bar"
        )
    )

    return {**state, "charts": charts}


def _make_chart(name: str, title: str, data: List[Dict], chart_type: str) -> ChartResult:
    result = generate_dashboard(data=data, title=title, chart_type=chart_type)
    billing = result["billing_source"]
    price = f"  (${result['amount_usd']:.2f})" if billing == "x402" else ""
    print(
        f"[chart]    {name:<18} → {result['dashboard_url']}   billing={billing}{price}"
    )
    return {
        "name": name,
        "dashboard_url": result["dashboard_url"],
        "embed_iframe": result["embed_iframe"],
        "billing_source": billing,
        "amount_usd": result["amount_usd"],
    }
