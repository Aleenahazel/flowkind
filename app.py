import streamlit as st

st.title("FlowKind – AI-Powered Customer Engagement Map")

# Step 1 – Business Snapshot
st.header("Step 1: Business Snapshot")

company_name = st.text_input("Company Name")

# Industry Section – General + Subcategory
industry_main = st.selectbox("Industry Category", [
    "Construction",
    "Health & Wellness",
    "Pet Services",
    "Education & Tutoring",
    "Home Services",
    "Retail (Physical & Online)",
    "Consulting & Coaching",
    "Events & Creative Services",
    "Legal & Financial Services",
    "Tech / SaaS / Online Tools",
    "Other"
])

# Subcategories based on the main industry
if industry_main == "Construction":
    industry_sub = st.selectbox("Specific Field", ["General Contractor", "Electrician", "Plumber", "HVAC", "Painter", "Other"])
elif industry_main == "Health & Wellness":
    industry_sub = st.selectbox("Specific Field", ["Physical Therapy", "Massage", "Yoga", "Reiki", "Chiropractor", "Other"])
elif industry_main == "Pet Services":
    industry_sub = st.selectbox("Specific Field", ["Dog Walking", "Grooming", "Training", "Boarding", "Vet", "Other"])
elif industry_main == "Education & Tutoring":
    industry_sub = st.selectbox("Specific Field", ["K–12 Tutoring", "Adult Education", "Test Prep", "Language Learning", "Homeschool Support", "Other"])
elif industry_main == "Home Services":
    industry_sub = st.selectbox("Specific Field", ["Cleaning", "Landscaping", "Interior Design", "Organizing", "Handyman", "Other"])
elif industry_main == "Retail (Physical & Online)":
    industry_sub = st.selectbox("Specific Field", ["Boutique", "eCommerce", "Bookstore", "Pop-up Vendor", "Other"])
elif industry_main == "Consulting & Coaching":
    industry_sub = st.selectbox("Specific Field", ["Business", "Marketing", "Life Coaching", "Career", "Spiritual", "Other"])
elif industry_main == "Events & Creative Services":
    industry_sub = st.selectbox("Specific Field", ["Photography", "Event Planning", "Design", "Catering", "Florals", "Other"])
elif industry_main == "Legal & Financial Services":
    industry_sub = st.selectbox("Specific Field", ["Bookkeeping", "Taxes", "Lawyer", "Notary", "Insurance", "Other"])
elif industry_main == "Tech / SaaS / Online Tools":
    industry_sub = st.selectbox("Specific Field", ["CRM", "Productivity App", "B2B SaaS", "AI Tool", "No-Code Platform", "Other"])
else:
    industry_sub = st.text_input("Please describe your industry")
location = st.text_input("Location (City or Region)")
team_size = st.selectbox("Team Size", ["Solo", "2–5", "6–15", "16–50", "50+"])
budget = st.radio("Budget Level", ["DIY", "Mid-Tier", "Enterprise"])
brand_voice = st.text_input("How would you describe your brand voice?")

# Step 2 – Engagement Goals
st.header("Step 2: Engagement Goals")

engagement_goals = st.multiselect(
    "What do you want to improve?",
    ["Onboarding → First Value", "Activation", "Upgrade/Upsell", "Reactivation", "Retention", "Referral", "Churn Recovery"]
)

kpis = st.text_input("What KPIs matter most to you?")
preferred_channels = st.multiselect(
    "Preferred communication channels",
    ["Email", "Chat", "Phone", "SMS", "In-App", "Slack", "Other"]
)

tools = st.multiselect(
    "Which tools do you use?",
    ["HubSpot", "Intercom", "Notion", "Airtable", "Zapier", "Freshworks", "Salesforce", "HoneyBook", "Other"]
)

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
    st.success("Form submitted! GPT prompt logic goes next.")
