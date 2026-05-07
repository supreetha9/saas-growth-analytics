"""SaaS Growth Intelligence Platform — Streamlit entry point."""

import streamlit as st

st.set_page_config(
    page_title="SaaS Growth Intelligence",
    page_icon="📊",
    layout="wide",
)

st.title("SaaS Growth Intelligence Platform")

st.markdown("""
**Activation, Retention, Churn, and Experimentation Analytics**

Use the sidebar to navigate between dashboard pages:

- **Executive Summary** — KPI cards, 30-day trends, and churn risk overview
- **Funnel Analysis** — Step-by-step conversion from signup to paid
- **Cohort Retention** — Weekly retention heatmap by signup cohort
- **Experimentation** — A/B test results for the onboarding experiment
""")

st.divider()

st.caption("Built with SQL (DuckDB), Python, and Streamlit")
