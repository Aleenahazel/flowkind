import streamlit as st
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG_ID")
)
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
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

# Generate the downloadable ZIP
create_downloadable_zip(prompt_text, mermaid_diagram)



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

