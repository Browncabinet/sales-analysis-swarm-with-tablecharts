# 📊 Sales Analysis Swarm with TableCharts

> A minimal, beginner-friendly **LangGraph agent swarm** that analyzes sales data
> and turns it into live, embeddable dashboards using
> [**TableCharts.co**](https://tablecharts.co) — the charting agent for AI agents.

<p align="center">
  <img src="https://tablecharts.co/og-image.png" alt="TableCharts dashboard preview" width="720" />
</p>

---

## 🚀 What this swarm does

Three cooperating agents run end-to-end with **zero human input**:

1. **📈 Analyst Agent** — reads a CSV of raw sales data and produces a plain-English summary
   (top region, best product, month-over-month growth).
2. **🎨 Chart Agent** — asks TableCharts to render **2–3 dashboards** (revenue by month,
   revenue by region, top products) and collects the live embed URLs.
3. **📝 Report Agent** — assembles a Markdown report with the summary + embedded
   dashboard URLs, ready to email, Slack, or drop into Notion.

Every chart is generated over a single HTTPS call. Dashboards **re-fetch source data
automatically**, so the report stays live.