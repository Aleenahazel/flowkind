import streamlit as st
from openai import OpenAI
import os
from utils import select_with_other

st.set_page_config(page_title="FlowKind", layout="centered")

# Title & tagline
st.title("FlowKind")
st.markdown("### *AI–Powered for Human Engagement*")

st.markdown("---")

# Agent options
agent_choice = st.selectbox(
    "Which agent would you like to run?",
    [
        "🧭 CEM Maker Agent",
        "🚀 Onboarding Agent",
        "🔁 Retention Agent",
        "💬 Support Agent",
        "👋 Offboarding Agent",
        "🧩 Full Engagement Engine (All)"
    ]
)

st.markdown("---")

# Route to the selected agent
if agent_choice == "🧭 CEM Maker Agent":
    from cem_maker_agent import run_cem_maker
    run_cem_maker()

elif agent_choice == "🚀 Onboarding Agent":
    from agents.onboarding_agent import run_onboarding_agent
    run_onboarding_agent()

elif agent_choice == "🔁 Retention Agent":
    from agents.retention_agent import run_retention_agent
    run_retention_agent()

elif agent_choice == "💬 Support Agent":
    from agents.support_agent import run_support_agent
    run_support_agent()

elif agent_choice == "👋 Offboarding Agent":
    from agents.offboarding_agent import run_offboarding_agent
    run_offboarding_agent()

elif agent_choice == "🧩 Full Engagement Engine (All)":
    from flowkind_conductor import run_full_engagement_engine
    run_full_engagement_engine()
else:
    st.warning("Select an agent to begin.")

