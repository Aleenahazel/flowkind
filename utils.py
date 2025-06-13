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
