import streamlit as st

def styled_text_input(label, value="", key=None, placeholder=None, on_change=None, disabled=False):
    """Creates a styled text input field."""
    input_style = f"""
        <style>
        div.stTextInput > div > div > input {{
            background-color: white;
            border: 1px solid var(--primary-color);
            border-radius: 5px;
            padding: 10px;
            color: var(--text-color);
        }}
        div.stTextInput > div > div > input:focus {{
            outline: none;
            box-shadow: 0 0 5px var(--primary-color);
        }}
        </style>
    """
    st.markdown(input_style, unsafe_allow_html=True)

    st.text_input(
        label,
        value=value,
        key=key,
        placeholder=placeholder,
        on_change=on_change,
        disabled=disabled,
        label_visibility="collapsed"
    ) 
