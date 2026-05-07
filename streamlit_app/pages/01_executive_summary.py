"""Executive Summary — KPI cards, trends, and churn risk overview."""

import pandas as pd
import plotly.express as px
import streamlit as st

from streamlit_app.utils.data_loader import load_churn_scores, load_daily_growth

st.set_page_config(page_title="Executive Summary", layout="wide")
st.header("Executive Summary")

df = load_daily_growth()
df = df[df["new_signups"] > 0].sort_values("metric_date")

last_30 = df.tail(30)
latest = last_30.iloc[-1]
prev = last_30.iloc[-2]

# ── KPI cards ────────────────────────────────────────────────────────────────

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(
    "Activation Rate",
    f"{latest['activation_rate']:.1%}",
    delta=f"{latest['activation_rate'] - prev['activation_rate']:.1%}",
)
col2.metric(
    "Trial → Paid",
    f"{latest['trial_to_paid_rate']:.1%}",
    delta=f"{latest['trial_to_paid_rate'] - prev['trial_to_paid_rate']:.1%}",
)
col3.metric(
    "D30 Retention",
    f"{latest['d30_retention_rate']:.1%}" if pd.notna(latest["d30_retention_rate"]) else "N/A",
)
col4.metric(
    "Churn Rate",
    f"{latest['churn_rate']:.1%}",
    delta=f"{latest['churn_rate'] - prev['churn_rate']:.1%}",
    delta_color="inverse",
)
col5.metric(
    "MRR",
    f"${latest['mrr']:,.0f}",
    delta=f"${latest['mrr'] - prev['mrr']:,.0f}",
)

# ── Trend chart ──────────────────────────────────────────────────────────────

st.subheader("30-Day KPI Trends")

trend_cols = ["activation_rate", "trial_to_paid_rate", "churn_rate"]
trend_data = last_30[["metric_date", *trend_cols]].melt(
    id_vars="metric_date", var_name="KPI", value_name="Rate"
)
trend_data["KPI"] = trend_data["KPI"].map(
    {
        "activation_rate": "Activation",
        "trial_to_paid_rate": "Trial→Paid",
        "churn_rate": "Churn",
    }
)

fig = px.line(trend_data, x="metric_date", y="Rate", color="KPI", markers=True)
fig.update_layout(yaxis_tickformat=".0%", xaxis_title="", yaxis_title="")
st.plotly_chart(fig, use_container_width=True)

# ── MRR trend ────────────────────────────────────────────────────────────────

st.subheader("Monthly Recurring Revenue")
fig_mrr = px.area(last_30, x="metric_date", y="mrr")
fig_mrr.update_layout(xaxis_title="", yaxis_title="MRR ($)", yaxis_tickprefix="$")
st.plotly_chart(fig_mrr, use_container_width=True)

# ── Churn risk summary ───────────────────────────────────────────────────────

st.subheader("Churn Risk Distribution")
churn = load_churn_scores()
risk_counts = churn["risk_tier"].value_counts().reindex(["low", "medium", "high"], fill_value=0)

c1, c2, c3 = st.columns(3)
c1.metric("Low Risk", f"{risk_counts.get('low', 0):,}")
c2.metric("Medium Risk", f"{risk_counts.get('medium', 0):,}")
c3.metric("High Risk", f"{risk_counts.get('high', 0):,}")
