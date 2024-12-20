# proj/src/ui/chat_ui.py

import streamlit as st
from typing import List, Dict, Optional
from datetime import datetime

class ChatUI:
    def __init__(self, ai_processor):
        """
        Initialize ChatUI with AI processor
        
        Args:
            ai_processor: AI processor instance (GeminiProcessor)
        """
        self.ai_processor = ai_processor
        self.initialize_chat_history()
    
    def initialize_chat_history(self):
        """Initialize chat history in session state if not present"""
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        if "chat_context" not in st.session_state:
            st.session_state.chat_context = {
                "video_insights": None,
                "current_topic": None
            }

    def update_chat_context(self, video_insights: Optional[Dict] = None):
        """
        Update the chat context with new video insights
        
        Args:
            video_insights (dict): Video analysis results
        """
        if video_insights:
            st.session_state.chat_context["video_insights"] = video_insights
            
            # Add a system message about the new video context
            self.add_message(
                "system",
                "New video analysis results are available for discussion. "
                "Feel free to ask questions about the video content!"
            )

    def add_message(self, role: str, content: str):
        """
        Add a new message to the chat history
        
        Args:
            role (str): Message role ('user', 'assistant', or 'system')
            content (str): Message content
        """
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({
            "role": role,
            "content": content,
            "timestamp": timestamp
        })

    def handle_user_input(self):
        """Handle user input and generate AI response"""
        if st.session_state.user_input:  # Access the input value from session state
            user_message = st.session_state.user_input
            
            # Add user message
            self.add_message("user", user_message)
            
            # Get AI response
            try:
                response = self.get_ai_response(user_message)
                self.add_message("assistant", response)
            except Exception as e:
                self.add_message(
                    "system",
                    f"Error getting response: {str(e)}"
                )
            
            # Clear input using session state
            st.session_state.user_input = ""

    def render_chat_interface(self):
        """Render the chat interface with message history and input"""
        # Chat container with custom styling
        chat_container = st.container()
        
        with chat_container:
            # Render message history
            for message in st.session_state.messages:
                self.render_message(message)

            # Chat input
            chat_input_container = st.container()
            
            with chat_input_container:
                # Create two columns for input and button
                col1, col2 = st.columns([5, 1])
                
                with col1:
                    # Use callback to handle input
                    st.text_input(
                        "Message AI Assistant",
                        key="user_input",  # Changed key to user_input
                        placeholder="Type your message here...",
                        label_visibility="collapsed",
                        on_change=self.handle_user_input  # Add callback
                    )
                
                with col2:
                    st.button(
                        "Send",
                        use_container_width=True,
                        on_click=self.handle_user_input  # Add callback to button
                    )

    def render_message(self, message: Dict):
        """
        Render a single chat message with appropriate styling
        
        Args:
            message (dict): Message dictionary with role, content, and timestamp
        """
        role = message["role"]
        content = message["content"]
        timestamp = message.get("timestamp", "")

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

    def get_ai_response(self, user_input: str) -> str:
        """
        Get AI response based on user input and current context
        
        Args:
            user_input (str): User's message
            
        Returns:
            str: AI response
        """
        # Get video context if available
        video_context = st.session_state.chat_context.get("video_insights")
        
        # Process response through AI processor
        response = self.ai_processor.generate_chat_response(
            user_input,
            video_context=video_context
        )
        
        return response

    def clear_chat_history(self):
        """Clear the chat history"""
        st.session_state.messages = []
        st.session_state.chat_context = {
            "video_insights": None,
            "current_topic": None
        }
