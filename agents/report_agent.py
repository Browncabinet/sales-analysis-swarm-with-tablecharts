"""Report agent — assembles a Markdown report with the summary and embed URLs."""
from __future__ import annotations

import os
from datetime import datetime, timezone

from .state import SwarmState

OUTPUT_DIR = "output"


def report_node(state: SwarmState) -> SwarmState:
    charts = state.get("charts", [])
    summary = state.get("summary", "")

    lines = [
        "# 📊 Sales Analysis Report",
        f"_Generated { datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC') } by the sales-analysis-swarm._",
        "",
        "## Summary",
        summary,
        "",
        "## Live dashboards",
        "_These embeds refetch data automatically — the report stays current._",
        "",
    ]

    for c in charts:
        lines.append(f"### {c['name'].replace('_', ' ').title()}")
        lines.append(f"- URL: <{c['dashboard_url']}>")
        lines.append(f"- Billing rail: `{c['billing_source']}`")
        lines.append("")
        lines.append(c["embed_iframe"])
        lines.append("")

    total_x402 = sum(c["amount_usd"] for c in charts if c["billing_source"] == "x402")
    lines.append("---")
    lines.append(
        f"**Billing:** {len(charts)} charts generated · "
        f"${total_x402:.2f} paid via x402 fallback."
    )
    lines.append("")
    lines.append("Powered by [TableCharts.co](https://tablecharts.co).")

    report_md = "\n".join(lines)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, "report.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(report_md)

    print(f"[report]   ✅ Report written to ./{path}")

    return {**state, "report_markdown": report_md, "report_path": path}
