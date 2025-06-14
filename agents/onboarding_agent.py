# agents/onboarding_agent.py

import os
from openai import OpenAI

def run_onboarding_agent(cem_base: str, user_inputs: str) -> dict:
    """
    Enhances the base CEM with onboarding-specific recommendations.
    Returns a dictionary with the output and optional diagram structure.
    """

    # Load context for onboarding
    with open("context/onboarding_context.txt", "r") as f:
        onboarding_context = f.read()

    # Build OpenAI client
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        organization=os.getenv("OPENAI_ORG_ID")
    )

    # Define system prompt
    system_prompt = f"""
You are an onboarding journey expert.

Use the following onboarding playbook and context to make detailed, high-impact suggestions for improving the onboarding portion of a Customer Engagement Map (CEM). Assume the reader is a founder or CX strategist at a small business.

Context:
{onboarding_context}
"""

    # Define user prompt
    user_prompt = f"""
Here's the base Customer Engagement Map:
---
{cem_base}

Here is additional business profile context:
---
{user_inputs}

Your task:
Suggest specific improvements for the onboarding stage (from signup to first value). Focus on messaging, channels, timing, automation, and behavioral nudges. Include any risks or blind spots. Use plain text.

Output should be clear and strategic — no headings needed.
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

    output = response.choices[0].message.content

    # Manually define flowchart nodes for now (replace with parsing later if needed)
    flowchart_nodes = [
    ("Start", "Signup"),
    ("Signup", "Welcome Email Sent"),
    ("Welcome Email Sent", "In-App Tour Shown"),
    ("In-App Tour Shown", "First Value Reached")
]

    return {
    "agent": "onboarding",
    "output": output,
    "flowchart_nodes": flowchart_nodes
}


