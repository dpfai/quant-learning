"""Sector-specific research prototype page."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from features.factors.sector.ad_tech_signals import digital_ad_spend_growth, ecpm_trend, platform_mix

st.set_page_config(page_title="Sector Research", page_icon="🏭", layout="wide")
st.title("Sector Research")
st.caption("Domain-informed signals are hypotheses until point-in-time validation proves otherwise.")

sector = st.selectbox("Sector lens", ["Ad Tech", "Consumer", "Supply Chain"])
st.subheader(f"{sector} Overview")
if sector == "Ad Tech":
    spend_growth = st.number_input("Digital ad spend growth", value=0.08, format="%.3f")
    ecpm_growth = st.number_input("eCPM growth", value=0.04, format="%.3f")
    owned_mix = st.slider("Owned/high-margin platform mix", 0.0, 1.0, 0.60)
    display = pd.DataFrame({"Factor": ["Digital ad spend growth", "eCPM trend", "Platform mix"], "Value": [digital_ad_spend_growth(1 + spend_growth, 1), ecpm_trend(1 + ecpm_growth, 1), platform_mix(owned_mix, 1)]})
else:
    display = pd.DataFrame({"Factor": ["Prototype status"], "Value": [0.0]})
    st.info("This sector currently exposes documented function signatures; connect point-in-time data before interpreting values.")
st.subheader("Sector-specific Factors")
st.dataframe(display, use_container_width=True, hide_index=True)
st.bar_chart(display.set_index("Factor"))
