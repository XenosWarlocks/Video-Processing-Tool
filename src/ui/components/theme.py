import streamlit as st

def apply_theme():
    """Applies the custom theme to the Streamlit app."""

    primary_color = "#3498db"  # Example: Blue
    secondary_color = "#2c3e50"  # Example: Dark Gray
    background_color = "#f4f4f4"
    text_color = "#262730"
    font = "sans-serif"

    st.markdown(
        f"""
        <style>
        :root {{
            --primary-color: {primary_color};
            --secondary-color: {secondary_color};
            --background-color: {background_color};
            --text-color: {text_color};
            --font: {font};
        }}
        html, body, [class*="css"] {{
            font-family: var(--font);
        }}
        .reportview-container .main {{
            background-color: var(--background-color);
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: var(--secondary-color);
        }}
        .stTextInput>div>div>input {{
            color: var(--text-color);
            border-color: var(--primary-color);
        }}
        .stButton>button {{
            background-color: var(--primary-color);
            color: white;
            border: none;
        }}
        .stButton>button:hover {{
            background-color: #2980b9;
        }}
        .stSlider>div>div {{
            background-color: var(--primary-color);
        }}
        .stProgress>div>div>div>div {{
            background-color: var(--primary-color);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    ) 