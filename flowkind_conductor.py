# flowkind_conductor.py

import streamlit as st
import zipfile
from io import BytesIO
from agents.onboarding_agent import run_onboarding_agent
from agents.retention_agent import run_retention_agent
from agents.support_agent import run_support_agent
from agents.offboarding_agent import run_offboarding_agent

def run_full_engagement_engine(cem_data: dict, selected_agents: list):
    st.info("🔍 Running selected engagement agents...")

all_outputs = {"CEM_Base.txt": cem_data["full_text_output"]}

    if "🚀 Onboarding Agent" in selected_agents:
        onboarding_output = run_onboarding_agent(cem_data)
        all_outputs["Onboarding_Agent.txt"] = onboarding_output

    if "🔁 Retention Agent" in selected_agents:
        retention_output = run_retention_agent(cem_data)
        all_outputs["Retention_Agent.txt"] = retention_output

    if "💬 Support Agent" in selected_agents:
        support_output = run_support_agent(cem_data)
        all_outputs["Support_Agent.txt"] = support_output

    if "👋 Offboarding Agent" in selected_agents:
        offboarding_output = run_offboarding_agent(cem_data)
        all_outputs["Offboarding_Agent.txt"] = offboarding_output

    st.success("🎉 All agents completed!")

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zf:
        for filename, content in all_outputs.items():
            zf.writestr(filename, content)
    zip_buffer.seek(0)

    st.download_button(
        label="📦 Download Full Engagement Engine ZIP",
        data=zip_buffer,
        file_name="flowkind_full_output.zip",
        mime="application/zip"
    )

