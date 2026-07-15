"""Analyst agent — reads the raw sales rows and produces a plain-English summary."""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, List

from .state import SwarmState


def analyst_node(state: SwarmState) -> SwarmState:
    rows: List[Dict] = state["rows"]

    total_revenue = sum(float(r["revenue"]) for r in rows)

    by_region: Dict[str, float] = defaultdict(float)
    by_product: Dict[str, float] = defaultdict(float)
    by_month: Dict[str, float] = defaultdict(float)

    for r in rows:
        by_region[r["region"]] += float(r["revenue"])
        by_product[r["product"]] += float(r["revenue"])
        by_month[r["month"]] += float(r["revenue"])

    top_region = max(by_region, key=by_region.get)
    top_product = max(by_product, key=by_product.get)

    months_sorted = sorted(by_month.keys())
    first_m, last_m = months_sorted[0], months_sorted[-1]
    growth = (by_month[last_m] - by_month[first_m]) / by_month[first_m] * 100

    summary = (
        f"Analyzed {len(rows)} rows across {len(by_region)} regions and "
        f"{len(by_product)} products. Total revenue **${total_revenue:,.0f}**. "
        f"Top region: **{top_region}**. Top product: **{top_product}**. "
        f"Revenue grew **{growth:+.1f}%** from {first_m} to {last_m}."
    )

    print(f"[analyst]  Summarized {len(rows)} rows across {len(by_region)} regions.")

    return {
        **state,
        "summary": summary,
        "stats": {
            "total_revenue": total_revenue,
            "top_region": top_region,
            "top_product": top_product,
            "growth_pct": round(growth, 1),
        },
    }
