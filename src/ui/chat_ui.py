# proj/src/ui/chat_ui.py

import streamlit as st
from typing import List, Dict, Optional
from datetime import datetime
from src.api.chat_api import ChatAPI
from src.ui.components.inputs import styled_text_input  # Import the styled input

class ChatUI:
    def __init__(self):
        """Initialize ChatUI with ChatAPI"""
        if 'chat_api' not in st.session_state:
            st.session_state.chat_api = ChatAPI()
        self.initialize_chat_history()
    
    def initialize_chat_history(self):
        """Initialize chat history in session state if not present"""
        if "chat_context" not in st.session_state:
            st.session_state.chat_context = {
                "video_insights": None,
                "current_topic": None
            }
        if "processing_message" not in st.session_state:
            st.session_state.processing_message = False

    def update_chat_context(self, video_insights: Optional[Dict] = None):
        """
        Update the chat context with new video insights
        
        Args:
            video_insights (dict): Video analysis results
        """
        if video_insights:
            st.session_state.chat_context["video_insights"] = video_insights
            
            # Add a system message using ChatAPI
            system_message = ("New video analysis results are available for discussion. "
                            "Feel free to ask questions about the video content!")
            st.session_state.chat_api.send_message(
                system_message,
                video_context=video_insights,
                is_system=True
            )

    def handle_user_input(self):
        """Handle user input and generate AI response"""
        # Check if already processing to prevent duplicate messages
        if st.session_state.processing_message:
            return

        if st.session_state.user_input:
            user_message = st.session_state.user_input
            video_context = st.session_state.chat_context.get("video_insights")
            
            try:
                # Set processing flag
                st.session_state.processing_message = True
                
                # Send message through ChatAPI
                response = st.session_state.chat_api.send_message(
                    user_message,
                    video_context=video_context
                )
                
                # Clear input and processing flag
                st.session_state.user_input = ""
                st.session_state.processing_message = False
                
                # Trigger rerender by updating session state
                st.session_state.last_message_time = datetime.now().isoformat()
                
            except Exception as e:
                st.error(f"Error getting response: {str(e)}")
                st.session_state.processing_message = False

    def render_chat_interface(self):
        """Render the chat interface with message history and input"""
        # Chat container with custom styling
        chat_container = st.container()
        
        with chat_container:
            # Display status while processing
            if st.session_state.processing_message:
                st.info("Processing your message...")
            
            # Render message history from ChatAPI
            messages = st.session_state.chat_api.get_chat_history()
            for message in messages:
                self.render_message(message)

            # Chat input
            chat_input_container = st.container()
            
            with chat_input_container:
                # Use the styled_text_input from components
                styled_text_input(
                    "Message AI Assistant",
                    key="user_input",
                    placeholder="Type your message here...",
                    on_change=self.handle_user_input,
                    disabled=st.session_state.processing_message,  # Disable while processing
                )

                # Use the primary_button from components (if needed)
                if st.button(
                    "Send",
                    disabled=st.session_state.processing_message,
                    on_click=self.handle_user_input
                ):
                    pass  # The on_click is handled by the styled_text_input's on_change

    def render_message(self, message: Dict):
        """
        Render a single chat message with appropriate styling
        
        Args:
            message (dict): Message dictionary with role and content
        """
        role = message["role"]
        content = message["content"]
        timestamp = datetime.now().strftime("%H:%M")  # Current time for display

        # Define colors and icons for different roles
        role_styles = {
            "user": {"color": "#1abc9c", "icon": "👤"},
            "assistant": {"color": "#3498db", "icon": "🤖"},
            "system": {"color": "#95a5a6", "icon": "ℹ️"}
        }

        style = role_styles.get(role, {"color": "#95a5a6", "icon": "💭"})
        
        # Create message container with role-specific styling
        message_container = st.container()
        
        with message_container:
            st.markdown(
                f"""
                <div style="
                    padding: 1rem;
                    border-radius: 10px;
                    margin: 0.5rem 0;
                    background-color: {'#f8f9fa' if role == 'user' else 'white'};
                    border-left: 4px solid {style['color']};
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <div style="
                        display: flex;
                        justify-content: space-between;
                        margin-bottom: 0.5rem;
                    ">
                        <div style="
                            color: {style['color']};
                            font-weight: 600;
                        ">
                            {style['icon']} {role.capitalize()}
                        </div>
                        <div style="
                            color: #95a5a6;
                            font-size: 0.8rem;
                        ">
                            {timestamp}
                        </div>
                    </div>
                    <div style="color: #2c3e50;">
                        {content}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    def clear_chat_history(self):
        """Clear the chat history"""
        if 'chat_api' in st.session_state:
            st.session_state.chat_api.clear_history()
        st.session_state.chat_context = {
            "video_insights": None,
            "current_topic": None
        }
        st.session_state.processing_message = False