import streamlit as st
import zipfile
from io import BytesIO
from agents.onboarding_agent import run_onboarding_agent
from utils import generate_drawio, generate_strategy_pdf

def run_full_engagement_engine(cem_data: dict, selected_agents: list):
    st.info("🚀 Running selected engagement agents...")

    all_outputs = {
        "CEM_Base.txt": cem_data["full_text_output"]
    }

   if "🚀 Onboarding Agent" in selected_agents:
    onboarding_output = run_onboarding_agent(
        cem_data["full_text_output"],
        cem_data["summary"]
    )

    all_outputs["Onboarding_Agent.txt"] = onboarding_output["output"]

    drawio_xml = generate_drawio(onboarding_output["flowchart_nodes"])
    all_outputs["CEM_Map.drawio"] = drawio_xml

    # Generate PDF strategy report
    pdf_bytes = generate_strategy_pdf(cem_data["user_inputs"], onboarding_output)
    all_outputs["Onboarding_Strategy.pdf"] = pdf_bytes

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
