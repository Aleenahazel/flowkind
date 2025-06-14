import os
import streamlit as st
from openai import OpenAI
from utils import select_with_other
from cem_maker_agent import run_cem_maker
from flowkind_conductor import run_full_engagement_engine

# Configure the page
st.set_page_config(page_title="FlowKind", layout="centered")

# Load OpenAI Client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG_ID")
)

# Header
st.title("FlowKind")
st.markdown("### *AI-Powered for Human Engagement*")
st.markdown("---")

# Step 1 — Agent Selection
specialist_agent_choices = st.multiselect(
    "Which parts of the customer journey would you like to improve?",
    [
        "🚀 Onboarding Agent",
        "🔁 Retention Agent",
        "💬 Support Agent",
        "👋 Offboarding Agent"
    ]
)

# Step 2 — Business Snapshot
st.header("Step 2: Business Snapshot")

company_name = st.text_input("Company Name")

industry_main = select_with_other("Industry Category", [
    "Pet Care Services",
    "Home Maintenance",
    "Home Organization & Interior",
    "Health & Personal Homecare",
    "Landscaping & Lawncare",
    "Other Home-Based Services"
], key_suffix="industry_main")

# Subcategories
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

# Step 3 — Engagement Goals
st.header("Step 3: Engagement Goals")

engagement_goals = st.multiselect(
    "What do you want to improve?",
    ["Onboarding → First Value", "Activation", "Upgrade/Upsell", "Reactivation", "Retention", "Referral", "Churn Recovery"]
)

kpis = st.multiselect(
    "What KPIs matter most to you right now?",
    [
        "Activation Rate", "Time to First Value", "Onboarding Completion Rate",
        "Customer Retention Rate", "Churn Rate", "Engagement Frequency",
        "Conversion Rate", "Referral Rate", "Customer Lifetime Value (LTV)",
        "Net Promoter Score (NPS)", "Other"
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

# Initialize once to prevent double submission
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

if not st.session_state.form_submitted:
    if st.button("✨ Generate My Engagement Map"):
        if all([
            company_name,
            industry_main,
            industry_sub,
            location,
            team_size,
            budget,
            brand_voice,
            engagement_goals,
            kpis,
            preferred_channels,
            tools,
            team_roles
        ]):
            st.session_state.form_submitted = True

            with st.spinner("🔄 Creating your base engagement map..."):
                user_inputs = {
                    "company_name": company_name,
                    "industry_main": industry_main,
                    "industry_sub": industry_sub,
                    "location": location,
                    "team_size": team_size,
                    "budget": budget,
                    "brand_voice": brand_voice,
                    "engagement_goals": engagement_goals,
                    "kpis": kpis,
                    "preferred_channels": preferred_channels,
                    "tools": tools,
                    "team_roles": team_roles,
                    "personas": personas,
                    "content_types": content_types,
                    "challenges": challenges,
                }

                from cem_maker_agent import run_cem_maker
                cem_data = run_cem_maker(user_inputs)

                st.success("✅ Base Engagement Map created!")

                from flowkind_conductor import run_full_engagement_engine
                run_full_engagement_engine(cem_data, specialist_agent_choices)
        else:
        st.warning("🚧 Please complete all required fields before generating.")
        else:
        st.info("✅ Engagement Map already generated. Refresh or reset to start over.")

