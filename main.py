import streamlit as st
from openai import OpenAI
import os
from utils import select_with_other

st.set_page_config(page_title="FlowKind", layout="centered")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG_ID")
)
st.title("FlowKind")
st.markdown("### *AI–Powered for Human Engagement*")
st.markdown("---")

# Agent options
agent_choice = st.multiselect(
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

# Industry Section – General + Subcategory
# Industry Category (Home Services focused)
industry_main = select_with_other("Industry Category", [
    "Pet Care Services",
    "Home Maintenance",
    "Home Organization & Interior",
    "Health & Personal Homecare",
    "Landscaping & Lawncare",
    "Other Home-Based Services"
], key_suffix="industry_main")

# Subcategories based on selection
if industry_main == "Pet Care Services":
    industry_sub = select_with_other("Specific Field", [
        "Dog Walking", "Pet Sitting", "Boarding", "Training", "Grooming", "Mobile Vet / Wellness", "Other"
    ], key_suffix="pet_services")

elif industry_main == "Home Maintenance":
    industry_sub = select_with_other("Specific Field", [
        "Cleaning Services", "Handyman / Repairs", "HVAC", "Plumbing", "Electrical", "Painting",
        "Appliance Repair", "Pest Control", "Other"
    ], key_suffix="home_maintenance")

elif industry_main == "Home Organization & Interior":
    industry_sub = select_with_other("Specific Field", [
        "Home Organizer", "Interior Design", "Feng Shui / Styling", "Decluttering Consultant", "Other"
    ], key_suffix="home_org")

elif industry_main == "Health & Personal Homecare":
    industry_sub = select_with_other("Specific Field", [
        "Non-Medical Homecare", "Companionship Services", "In-Home Massage / Wellness",
        "Doulas / Postpartum Care", "Senior Support", "Other"
    ], key_suffix="homecare")

elif industry_main == "Landscaping & Lawncare":
    industry_sub = select_with_other("Specific Field", [
        "Lawn Mowing", "Snow Removal", "Landscape Design", "Tree / Shrub Maintenance",
        "Gutter / Outdoor Cleaning", "Other"
    ], key_suffix="landscaping")

else:
    industry_sub = select_with_other("Specific Field", ["Other"], key_suffix="other_catchall")

location = st.text_input("Location (City or Region)")
team_size = st.selectbox("Team Size", ["Solo", "2–5", "6–15", "16–50", "50+"])
budget = st.radio("Budget Level", [
    "DIY ($0–$500/month)", 
    "Small ($500–$2,000/month)", 
    "Mid-Tier ($2,000–$10,000/month)", 
    "Enterprise ($10,000+/month)"
])
brand_voice = st.text_input("How would you describe your brand voice?")

# Step 2 – Engagement Goals
st.header("Step 2: Engagement Goals")

engagement_goals = st.multiselect(
    "What do you want to improve?",
    ["Onboarding → First Value", "Activation", "Upgrade/Upsell", "Reactivation", "Retention", "Referral", "Churn Recovery"]
)

kpis = st.multiselect(
    "What KPIs matter most to you right now?",
    [
        "Activation Rate",
        "Time to First Value",
        "Onboarding Completion Rate",
        "Customer Retention Rate",
        "Churn Rate",
        "Engagement Frequency",
        "Conversion Rate",
        "Referral Rate",
        "Customer Lifetime Value (LTV)",
        "Net Promoter Score (NPS)",
        "Other"
    ]
)

if "Other" in kpis:
    other_kpi = st.text_input("Please describe your custom KPI")
    if other_kpi:
        kpis.append(other_kpi)


preferred_channels = st.multiselect(
    "Preferred communication channels",
    ["Email", "Chat", "Phone", "SMS", "In-App", "Slack", "Other"]
)

tools = st.multiselect(
    "Which tools do you use?",
    ["HubSpot", "Intercom", "Notion", "Airtable", "Zapier", "Freshworks", "Salesforce", "HoneyBook", "Other"]
)

if "Other" in tools:
    other_tools = st.text_input("Please enter additional tools separated by commas")
    if other_tools:
        additional = [tool.strip() for tool in other_tools.split(",") if tool.strip()]
        tools.extend(additional)

team_roles = st.text_input("What roles are on your team? (e.g., CSM, Support, Marketing)")

deep_dive = st.checkbox("Add more detail for a smarter output")

if deep_dive:
    st.subheader("Optional: Deeper Strategy Questions")
    personas = st.text_area("Who are your customer personas?")
    content_types = st.text_input("What content works best for your audience?")
    challenges = st.text_area("What’s your biggest engagement or handoff challenge?")
else:
    personas = ""
    content_types = ""
    challenges = ""

if st.button("Generate My Engagement Map"):
    st.success("Form submitted! Generating outputs...")

st.success("Generating engagement map with AI...")

# Combine all user inputs into a structured summary
user_inputs = f"""
Company Name: {company_name}
Industry: {industry_main} - {industry_sub}
Location: {location}
Team Size: {team_size}
Budget: {budget}
Brand Voice: {brand_voice}

Engagement Goals: {', '.join(engagement_goals)}
Key KPIs: {kpis}
Preferred Channels: {', '.join(preferred_channels)}
Tools Used: {', '.join(tools)}
Team Roles: {team_roles}

Personas: {personas}
Content Types: {content_types}
Challenges: {challenges}
"""
# Role prompt with strategic frameworks
system_prompt = """
You are a senior customer experience strategist and service designer.
You specialize in building human-centered, high-conversion customer engagement flows that align with Jobs To Be Done, the HEART UX framework, and behavioral science principles (BJ Fogg, Kahneman).

You blend strategic brand positioning (Simon Sinek, Marty Neumeier, Seth Godin) with UX and research best practices (IDEO, Erika Hall), using service design methods (Stickdorn) and bot design logic (Amir Shevat) to map real-life journeys across key touchpoints.

Your job is to guide small businesses with limited budgets through meaningful, scalable engagement strategies.
"""

# User prompt with detailed output instructions
user_prompt = f"""
Using the following business profile:

{user_inputs}

Generate a complete Customer Engagement Map. Your output should include:

1. A written breakdown of each engagement stage (e.g., Awareness → First Value → Activation → Retention → Advocacy)
   - Goals of that stage
   - Primary customer actions or thoughts (Jobs To Be Done style)
   - Key team roles or tools involved
   - Preferred channels or formats (e.g., SMS, email, in-person)

2. Additional Recommendations
   - Brand tone and behavior suggestions
   - Follow-up logic or automation ideas
   - Metrics to monitor (HEART or business KPIs)
   - Sustainability tips for small teams

3. A Mermaid.js-compatible flowchart showing the journey structure and key decisions.

Use clear, strategic language and assume the reader is a founder or early ops hire.
"""

# Call OpenAI
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.7,
)

full_output = response.choices[0].message.content

# Separate flowchart if possible
if "```mermaid" in full_output:
    parts = full_output.split("```mermaid")
    prompt_text = parts[0].strip()
    mermaid_diagram = parts[1].split("```")[0].strip()
else:
    prompt_text = full_output
    mermaid_diagram = "graph TD\nA[Start] --> B[Mermaid Diagram Not Detected]"


import zipfile
from io import BytesIO

def create_downloadable_zip(prompt_text, mermaid_diagram):
    prompt_bytes = BytesIO()
    prompt_bytes.write(prompt_text.encode('utf-8'))
    prompt_bytes.seek(0)

    mermaid_bytes = BytesIO()
    mermaid_bytes.write(f"```mermaid\n{mermaid_diagram}\n```".encode('utf-8'))
    mermaid_bytes.seek(0)

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("prompt.txt", prompt_bytes.read())
        zf.writestr("flowchart.md", mermaid_bytes.read())
    zip_buffer.seek(0)

    st.download_button(
        label="📦 Download CEM Output as ZIP",
        data=zip_buffer,
        file_name="flowkind_output.zip",
        mime="application/zip"
    )

# Generate the downloadable ZIP
create_downloadable_zip(prompt_text, mermaid_diagram)
