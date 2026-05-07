"""Experimentation — A/B test results for onboarding_v2."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from python.src.analysis import analyze_experiment
from streamlit_app.utils.data_loader import load_experiment_results

st.set_page_config(page_title="Experimentation", layout="wide")
st.header("Experimentation: Onboarding V2")

exp_df = load_experiment_results()
results = analyze_experiment(exp_df)

r = results.iloc[0]

# ── Significance banner ─────────────────────────────────────────────────────

if r["significant"]:
    st.success(
        f"Statistically significant result (p = {r['p_value']:.6f}). "
        f"Treatment lifts activation by {r['absolute_lift']:.1%} ({r['relative_lift']:.1%} relative)."
    )
else:
    st.warning(
        f"Not statistically significant (p = {r['p_value']:.4f}). "
        "More data is needed before rolling out the treatment."
    )

# ── Side-by-side metrics ────────────────────────────────────────────────────

col1, col2, col3 = st.columns(3)
col1.metric("Control Activation", f"{r['control_rate']:.1%}", help=f"n = {r['control_users']:,}")
col2.metric(
    "Treatment Activation", f"{r['treatment_rate']:.1%}", help=f"n = {r['treatment_users']:,}"
)
col3.metric("Absolute Lift", f"{r['absolute_lift']:.1%}")

# ── Bar chart with confidence intervals ──────────────────────────────────────

st.subheader("Activation Rates by Variant")


def _ci(rate: float, n: int) -> float:
    """95% confidence interval half-width for a proportion."""
    return 1.96 * np.sqrt(rate * (1 - rate) / n)


control_ci = _ci(r["control_rate"], r["control_users"])
treatment_ci = _ci(r["treatment_rate"], r["treatment_users"])

fig = go.Figure()
fig.add_trace(
    go.Bar(
        x=["Control", "Treatment"],
        y=[r["control_rate"], r["treatment_rate"]],
        error_y=dict(type="data", array=[control_ci, treatment_ci], visible=True),
        marker_color=["#636EFA", "#00CC96"],
        text=[f"{r['control_rate']:.1%}", f"{r['treatment_rate']:.1%}"],
        textposition="outside",
    )
)
fig.update_layout(
    yaxis_tickformat=".0%",
    yaxis_title="Activation Rate",
    xaxis_title="Variant",
    height=400,
)
st.plotly_chart(fig, use_container_width=True)

# ── Details table ────────────────────────────────────────────────────────────

st.subheader("Full Results")
st.dataframe(results, hide_index=True)
