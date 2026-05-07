"""Funnel Analysis — step-by-step conversion visualization."""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from python.src.analysis import analyze_funnel
from streamlit_app.utils.data_loader import load_funnel

st.set_page_config(page_title="Funnel Analysis", layout="wide")
st.header("Funnel Analysis")

funnel_raw = load_funnel()

# ── Channel filter ───────────────────────────────────────────────────────────

channels = (
    funnel_raw.dropna(subset=["acquisition_channel"])["acquisition_channel"].unique().tolist()
)
selected = st.selectbox("Acquisition Channel", ["All", *sorted(channels)])

if selected == "All":
    display_df = funnel_raw[funnel_raw["acquisition_channel"].isna()]
else:
    display_df = funnel_raw[funnel_raw["acquisition_channel"] == selected]

funnel = analyze_funnel(
    funnel_raw
    if selected == "All"
    else funnel_raw[funnel_raw["acquisition_channel"].isin([selected, None])]
)

# ── Funnel bar chart ─────────────────────────────────────────────────────────

st.subheader("Conversion Funnel")

fig = go.Figure(
    go.Funnel(
        y=funnel["step"],
        x=funnel["users"],
        textinfo="value+percent initial",
        marker=dict(color=["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A"]),
    )
)
fig.update_layout(funnelmode="stack", height=400)
st.plotly_chart(fig, use_container_width=True)

# ── Step-by-step metrics ─────────────────────────────────────────────────────

st.subheader("Step-by-Step Conversion")
cols = st.columns(len(funnel))
for i, (_, row) in enumerate(funnel.iterrows()):
    with cols[i]:
        st.metric(row["step"].title(), f"{row['users']:,}")
        if i > 0:
            st.caption(f"Step rate: {row['step_rate']:.1%}")
            st.caption(f"Drop-off: {row['drop_off']:.1%}")

# ── Channel comparison ───────────────────────────────────────────────────────

if selected == "All":
    st.subheader("Conversion by Channel")
    by_channel = funnel_raw.dropna(subset=["acquisition_channel"])
    fig2 = px.bar(
        by_channel,
        x="acquisition_channel",
        y="overall_conversion_rate",
        text_auto=".1%",
        color="acquisition_channel",
    )
    fig2.update_layout(
        xaxis_title="Channel",
        yaxis_title="Overall Conversion Rate",
        yaxis_tickformat=".0%",
        showlegend=False,
    )
    st.plotly_chart(fig2, use_container_width=True)
