import streamlit as st
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG_ID")
)

def run_cem_maker(user_inputs: dict) -> dict:
    summary = f"""
    Company Name: {user_inputs['company_name']}
    Industry: {user_inputs['industry_main']} - {user_inputs['industry_sub']}
    Location: {user_inputs['location']}
    Team Size: {user_inputs['team_size']}
    Budget: {user_inputs['budget']}
    Brand Voice: {user_inputs['brand_voice']}
    
    Engagement Goals: {', '.join(user_inputs['engagement_goals'])}
    Key KPIs: {user_inputs['kpis']}
    Preferred Channels: {', '.join(user_inputs['preferred_channels'])}
    Tools Used: {', '.join(user_inputs['tools'])}
    Team Roles: {user_inputs['team_roles']}
    
    Personas: {user_inputs['personas']}
    Content Types: {user_inputs['content_types']}
    Challenges: {user_inputs['challenges']}
    """

    system_prompt = """
    You are a senior customer experience strategist and service designer.
    You specialize in building human-centered, high-conversion customer engagement flows that align with Jobs To Be Done, the HEART UX framework, and behavioral science principles (BJ Fogg, Kahneman).
    
    You blend strategic brand positioning (Simon Sinek, Marty Neumeier, Seth Godin) with UX and research best practices (IDEO, Erika Hall), using service design methods (Stickdorn) and bot design logic (Amir Shevat) to map real-life journeys across key touchpoints.
    
    Your job is to guide small businesses with limited budgets through meaningful, scalable engagement strategies.
    """

    user_prompt = f"""
    Using the following business profile:

    {summary}

    Generate a base Customer Engagement Map. Your output should include:

    1. A written breakdown of each engagement stage (e.g., Awareness → First Value → Activation → Retention → Advocacy)
       - Goals of that stage
       - Primary customer actions or thoughts (Jobs To Be Done style)
       - Key team roles or tools involved
       - Preferred channels or formats (e.g., SMS, email, in-product)

    2. Additional Recommendations
       - Brand tone and behavior suggestions
       - Follow-up logic or automation ideas
       - Metrics to monitor (HEART or business KPIs)
       - Scalability tips for SaaS founders

    3. A logical flow structure for turning this into a visual diagram (for draw.io or other software).
       - Include a simple list of nodes and connections.
       - Use plain text, not code formatting.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
    )

    full_output = response.choices[0].message.content

    return {
        "summary": summary,
        "full_text_output": full_output,
        "user_inputs": user_inputs
    }
