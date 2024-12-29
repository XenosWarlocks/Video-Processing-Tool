import streamlit as st

def primary_button(label, key=None, on_click=None, disabled=False):
    """Creates a primary styled button."""
    button_style = f"""
        <style>
        div.stButton > button:first-child {{
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: 600;
        }}
        div.stButton > button:hover {{
            background-color: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)
    st.button(
        label,
        key=key,
        on_click=on_click,
        disabled=disabled
    )

def secondary_button(label, key=None, on_click=None, disabled=False):
    """Creates a secondary styled button."""
    button_style = f"""
        <style>
        div.stButton > button:first-child {{
            background-color: var(--secondary-color);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: 600;
        }}
        div.stButton > button:hover {{
            background-color: #1a232e;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)
    st.button(
        label,
        key=key,
        on_click=on_click,
        disabled=disabled
    )
