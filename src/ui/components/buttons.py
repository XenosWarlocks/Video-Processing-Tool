import streamlit as st

def primary_button(label, key=None, on_click=None, disabled=False):
    """Creates a primary styled button."""
    st.button(
        label,
        key=key,
        on_click=on_click,
        disabled=disabled,
        css=f"""
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: 600;
            &:hover {{
                background-color: #2980b9;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }}
        """,
    )

def secondary_button(label, key=None, on_click=None, disabled=False):
    """Creates a secondary styled button."""
    st.button(
        label,
        key=key,
        on_click=on_click,
        disabled=disabled,
        css=f"""
            background-color: var(--secondary-color);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: 600;
            &:hover {{
                background-color: #1a232e;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }}
        """,
    ) 