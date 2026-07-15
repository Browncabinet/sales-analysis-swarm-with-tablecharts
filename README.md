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

---

## 💳 Autonomous billing (credits first, then $0.59 x402)

The agent doesn't need a human to top up a card. TableCharts bills like this:


|
Order
|
Rail
|
Notes
|
|
-----
|
----
|
-----
|
|
1
|
Weekly subscription quota
|
If you have an active plan, it's used first.
|
|
2
|
Prepaid bundle credits
|
Bought once from
`tablecharts.co/pricing`
, never expire.
|
|
3
|
**
x402 fallback — $0.59 / chart
**
|
If both are empty, the agent pays per chart in USDC on Base.
|

The API returns an `X-Chart-Billing` header (`weekly`, `prepaid`, or `x402`) so you can
observe exactly how each chart was paid for. The tool in this repo prints it on every
call.

---

## ⚡ Setup (under 2 minutes)

```bash
# 1. Clone
git clone https://github.com/Browncabinet/sales-analysis-swarm-with-tablecharts.git

# 2. Install
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. Add your TableCharts API key
cp .env.example .env
# then open .env and paste your key from https://tablecharts.co/dashboard/api-keys

# 4. Run the swarm
python main.py
```

You'll see something like:

```
[analyst]  Summarized 12 rows across 3 regions.
[chart]    revenue_by_month   → https://tablecharts.co/embed/8f3a...   billing=prepaid
[chart]    revenue_by_region  → https://tablecharts.co/embed/2b7c...   billing=prepaid
[chart]    top_products       → https://tablecharts.co/embed/91ee...   billing=x402  ($0.59)
[report]   ✅ Report written to ./output/report.md
```

---

## 📁 Repo structure

```
sales-analysis-swarm-with-tablecharts/
├── agents/
│   ├── __init__.py
│   ├── state.py             # shared LangGraph state
│   ├── analyst_agent.py     # summarizes the raw sales data
│   ├── chart_agent.py       # calls TableCharts for each dashboard
│   ├── report_agent.py      # assembles the final Markdown report
│   └── tablecharts_tool.py  # thin, well-commented TableCharts client
├── data/
│   └── sales.csv            # sample sales data
├── output/                  # generated report lands here
├── main.py                  # wires the LangGraph pipeline
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🧩 Adapt it to your own data

- Swap `data/sales.csv` for any CSV (marketing spend, support tickets, product usage…).
- Edit `agents/chart_agent.py` to change which charts you want — TableCharts auto-picks
  the best of 25+ chart types, or you can pass `chart_type` explicitly.
- Add more nodes to the graph (forecasting agent, anomaly-detection agent) — they can
  all reuse `tablecharts_tool.py` to visualize their output.

---

## 🔗 Links

- **TableCharts.co** — https://tablecharts.co
- **API docs** — https://tablecharts.co/docs
- **Pricing** — https://tablecharts.co/pricing (bundles from **$9**, x402 fallback at **$0.59/chart**)
- **Agent Card (A2A)** — https://tablecharts.co/.well-known/agent-card.json

MIT licensed — fork it, remix it, ship it.
