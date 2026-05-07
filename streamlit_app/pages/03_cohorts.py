"""Cohort Retention — weekly retention heatmap."""

import plotly.express as px
import streamlit as st

from python.src.analysis import build_cohort_heatmap
from streamlit_app.utils.data_loader import load_cohort_retention

st.set_page_config(page_title="Cohort Retention", layout="wide")
st.header("Cohort Retention")

cohort_df = load_cohort_retention()
heatmap = build_cohort_heatmap(cohort_df)

# ── Controls ─────────────────────────────────────────────────────────────────

num_cohorts = st.slider("Number of cohorts to display", 5, len(heatmap), min(20, len(heatmap)))
display = heatmap.head(num_cohorts)

# ── Heatmap ──────────────────────────────────────────────────────────────────

st.subheader(f"Retention Heatmap (first {num_cohorts} weekly cohorts)")

fig = px.imshow(
    display.values,
    x=display.columns.tolist(),
    y=display.index.tolist(),
    color_continuous_scale="Blues",
    zmin=0,
    zmax=1,
    text_auto=".0%",
    aspect="auto",
)
fig.update_layout(
    xaxis_title="Weeks Since Signup",
    yaxis_title="Signup Cohort Week",
    height=max(400, num_cohorts * 28),
)
st.plotly_chart(fig, use_container_width=True)

# ── Cohort sizes ─────────────────────────────────────────────────────────────

st.subheader("Cohort Sizes")
sizes = cohort_df[cohort_df["weeks_since_signup"] == 0][["cohort_week", "cohort_size"]].head(
    num_cohorts
)
sizes["cohort_week"] = sizes["cohort_week"].astype(str)
st.dataframe(
    sizes.rename(columns={"cohort_week": "Cohort Week", "cohort_size": "Users"}), hide_index=True
)
