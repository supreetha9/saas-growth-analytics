# SaaS Growth Intelligence Platform

**Activation, Retention, Churn, and Experimentation Analytics**

An end-to-end analytics project that models 1.4M+ product events for a B2B SaaS company, defines core growth KPIs, runs a statistically rigorous A/B test, and delivers an interactive Streamlit dashboard — all in SQL and Python.

---

## Business Problem

A B2B SaaS company has strong signups but weak paid conversion. Leadership needs answers to five questions:

1. Which users activate?
2. Which onboarding steps cause the biggest drop-off?
3. Which features predict paid conversion?
4. Did the new onboarding experiment improve activation?
5. Which accounts are at risk of churning?

## Key Findings

| Finding | Detail |
| --- | --- |
| Funnel bottleneck | 33% drop-off between invite sent and first project |
| Overall conversion | 15.7% of signups reach paid |
| Experiment lift | New onboarding flow lifts activation by **3.2%** (p < 0.001) |
| Churn risk | Logistic regression identifies at-risk accounts by recency and engagement depth |
| Best channel | Referral converts at the highest rate |

## Tech Stack

| Layer | Tool |
| --- | --- |
| Data generation | Python (NumPy, Faker) |
| SQL modeling | DuckDB (staging views + analytical marts) |
| Analysis | pandas, statsmodels, scikit-learn |
| Dashboard | Streamlit + Plotly |
| Documentation | Sphinx (reStructuredText) |
| Environment | pyenv + hatchling |

## Architecture

```
Synthetic Data (Parquet)
    ↓  generate_data.py
DuckDB SQL Staging Views
    ↓  stg_*.sql
DuckDB SQL Mart Tables
    ↓  mart_*.sql → Parquet exports
Python Analysis
    ↓  analysis.py (funnel, cohort, A/B test, churn)
Streamlit Dashboard
    └  4 interactive pages
```

## Quick Start

**Prerequisites:** [pyenv](https://github.com/pyenv/pyenv) with pyenv-virtualenv.

```bash
# 1. Create the virtual environment
pyenv install -s 3.13.3
pyenv virtualenv 3.13.3 saas_env
pyenv local saas_env

# 2. Install all dependencies
make all-env

# 3. Run the full pipeline (generate data → SQL transforms → analysis)
make pipeline

# 4. Launch the dashboard
make app
```

The dashboard opens at [http://localhost:8501](http://localhost:8501).

Run `make help` to see all available targets.

## Dashboard Pages

| Page | What it shows |
| --- | --- |
| Executive Summary | KPI cards (activation, conversion, retention, churn, MRR), 30-day trends, churn risk breakdown |
| Funnel Analysis | Step-by-step conversion funnel with channel filter and drop-off rates |
| Cohort Retention | Weekly retention heatmap colored by rate, with cohort size annotations |
| Experimentation | Control vs treatment comparison, confidence intervals, p-value, significance banner |

## Project Structure

```
saas-growth-analytics/
├── Makefile                    # pyenv-aware build targets
├── pyproject.toml              # dependencies + tool config
├── .python-version             # locks pyenv virtualenv
│
├── data/
│   ├── raw/                    # generated Parquet files (gitignored)
│   ├── processed/              # mart Parquet exports (gitignored)
│   └── sample/                 # small CSV samples for inspection
│
├── sql/
│   ├── staging/                # DuckDB staging views (clean + cast)
│   └── marts/                  # analytical mart tables
│
├── python/
│   └── src/
│       ├── generate_data.py    # synthetic data generator
│       ├── run_sql_models.py   # DuckDB SQL runner
│       ├── analysis.py         # funnel, cohort, A/B test, churn
│       └── metrics.py          # KPI helpers
│
├── streamlit_app/
│   ├── app.py                  # entry point
│   ├── pages/                  # multi-page dashboard
│   └── utils/                  # cached data loaders
│
└── docs/                       # Sphinx documentation (.rst)
```

## Core KPIs

| KPI | Definition |
| --- | --- |
| Signup-to-activation rate | Users who complete workspace creation within 7 days |
| Trial-to-paid conversion | Trial users who become paying customers |
| D1 / D7 / D30 retention | Users active 1, 7, or 30 days after signup |
| Churn rate | Paying users who cancel in a period |
| MRR | Monthly recurring revenue from active subscriptions |
| Experiment lift | Activation rate difference between control and treatment |

## Documentation

Full project documentation is built with Sphinx:

```bash
make docs        # live-reload server on port 8000
make docs-build  # one-shot HTML build to docs/_build/html
```

## License

MIT
