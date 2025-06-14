# utils.py

import streamlit as st

def select_with_other(label, options, key_suffix=""):
    """
    Streamlit selectbox that adds a text input if 'Other' is selected.
    Returns the selected option or the custom 'Other' input.
    """
    selection = st.selectbox(label, options, key=f"{label}_select_{key_suffix}")
    if selection == "Other":
        other_input = st.text_input(f"Please describe your '{label.lower()}'", key=f"{label}_other_{key_suffix}")
        if other_input:
            return other_input
    return selection

def generate_drawio(nodes: list[tuple[str, str]]) -> str:
    """
    Converts a list of (from, to) node connections into draw.io-compatible XML.
    Returns XML string for .drawio file.
    """
    xml_header = '''<?xml version="1.0" encoding="UTF-8"?><mxfile><diagram name="CEM Map" id="cem-map-1"><mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>'''
    xml_footer = '''</root></mxGraphModel></diagram></mxfile>'''

    cells = []
    id_counter = 2
    node_ids = {}

    for from_node, to_node in nodes:
        for node in [from_node, to_node]:
            if node not in node_ids:
                node_id = str(id_counter)
                node_ids[node] = node_id
                x_offset = id_counter * 150
                cell = f'''
<mxCell id="{node_id}" value="{node}" style="rounded=1;whiteSpace=wrap;" vertex="1" parent="1">
  <mxGeometry x="{x_offset}" y="100" width="140" height="60" as="geometry"/>
</mxCell>'''
                cells.append(cell)
                id_counter += 1

        edge_id = str(id_counter)
        edge = f'''
<mxCell id="{edge_id}" style="endArrow=block;" edge="1" parent="1" source="{node_ids[from_node]}" target="{node_ids[to_node]}">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>'''
        cells.append(edge)
        id_counter += 1

    return xml_header + ''.join(cells) + xml_footer

from fpdf import FPDF

def generate_strategy_pdf(user_inputs: dict, agent_output: dict) -> bytes:
    """
    Creates a PDF from user_inputs and onboarding agent recommendations.
    Returns PDF as a bytes object.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "FlowKind: Onboarding Strategy Report", ln=True, align='C')
    pdf.ln(10)

    # Section: Business Snapshot
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Business Snapshot", ln=True)
    pdf.set_font("Arial", "", 11)
    for key, value in user_inputs.items():
        if value:
            label = key.replace("_", " ").title()
            pdf.multi_cell(0, 8, f"{label}: {value}")
    pdf.ln(5)

    # Section: Recommendations
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Onboarding Agent Recommendations", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, agent_output["output"])

    return pdf.output(dest="S").encode("latin1")

