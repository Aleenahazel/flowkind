import streamlit as st
import zipfile
from io import BytesIO
from agents.onboarding_agent import run_onboarding_agent

def run_full_engagement_engine(cem_data: dict, selected_agents: list):
    st.info("🚀 Running selected engagement agents...")

    all_outputs = {
        "CEM_Base.txt": cem_data["full_text_output"]
    }

    if "🚀 Onboarding Agent" in selected_agents:
        onboarding_output = run_onboarding_agent(cem_data)
        all_outputs["Onboarding_Agent.txt"] = onboarding_output
        st.success("✅ Onboarding Agent completed!")

    # Placeholder for future agents:
    # if "🔁 Retention Agent" in selected_agents:
    #     ...

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zf:
        for filename, content in all_outputs.items():
            zf.writestr(filename, content)
    zip_buffer.seek(0)

    st.download_button(
        label="📦 Download Engagement Output ZIP",
        data=zip_buffer,
        file_name="flowkind_output.zip",
        mime="application/zip"
    )
