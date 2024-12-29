import streamlit as st

def card(title, content, icon=None):
    """Creates a styled card component."""
    with st.container():
        st.markdown(
            f"""
            <div class="card">
                {f'<div class="card-icon">{icon}</div>' if icon else ''}
                <div class="card-title">{title}</div>
                <div class="card-content">{content}</div>
            </div>
            <style>
            .card {{
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                padding: 20px;
                margin-bottom: 15px;
                display: flex;
                align-items: center;
            }}
            .card-icon {{
                font-size: 24px;
                margin-right: 15px;
                color: var(--primary-color);
            }}
            .card-title {{
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 10px;
                color: var(--secondary-color);
            }}
            .card-content {{
                font-size: 14px;
                color: var(--text-color);
            }}
            </style>
            """,
            unsafe_allow_html=True,
        ) 