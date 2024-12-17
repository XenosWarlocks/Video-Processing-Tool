# proj/src/ui/streamlit.py
import streamlit as st
import base64
from typing import List, Dict, Any
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from datetime import datetime

from src.core.config_manager import ConfigManager
from src.video_processing.video_handler import VideoProcessor
from src.ai_integration.gemini_processor import GeminiProcessor

class EnhancedStreamlitApp:
    def __init__(self):
        """
        Initialize Streamlit application with advanced features and design
        """
        self.config_manager = ConfigManager()
        self.video_processor = VideoProcessor(self.config_manager)
        self.ai_processor = GeminiProcessor(self.config_manager)
        
        self._setup_page_config()
        self._apply_custom_styling()
    
    def _setup_page_config(self):
        """
        Configure Streamlit page layout and advanced styling
        """
        st.set_page_config(
            page_title="🎬 EduVision: AI Video Insights",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def _apply_custom_styling(self):
        """
        Apply advanced custom CSS for a more modern and appealing design
        """
        st.markdown("""
        <style>
            /* Global Background */
            .reportview-container {
                background: linear-gradient(135deg, #f4f4f4, #e8e8e8);
                font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
            }
            
            /* Card-like Containers */
            .stCard {
                background-color: white;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                padding: 20px;
                transition: all 0.3s ease;
            }
            
            /* Sidebar Enhancements */
            .css-1aumxhk {
                background: linear-gradient(160deg, #ffffff, #f0f0f0);
                border-right: 1px solid #e0e0e0;
            }
            
            /* Button Styling */
            .stButton>button {
                background-color: #3498db;
                color: white;
                border-radius: 8px;
                border: none;
                padding: 10px 20px;
                font-weight: 600;
                transition: all 0.3s ease;
                text-transform: uppercase;
            }
            
            .stButton>button:hover {
                background-color: #2980b9;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }
            
            /* File Uploader */
            .stFileUploader {
                background-color: #f8f9fa;
                border: 2px dashed #3498db;
                border-radius: 12px;
                padding: 20px;
                text-align: center;
            }
            
            /* Expanders */
            .streamlit-expanderHeader {
                background-color: #f1f3f4;
                border-radius: 8px;
                font-weight: 600;
            }
            
            /* Typography */
            h1, h2, h3 {
                color: #2c3e50;
                font-weight: 700;
            }
        </style>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """
        Create an interactive and visually appealing sidebar
        """
        with st.sidebar:
            st.image("C:\Users\\mannu\\Downloads\\JSproj\\megaProj\\vid_pro_tool\\assets\\logo.jpg", width=250)  # Add a logo
            st.markdown("## 🎥 EduVision Settings")
            
            st.markdown("### Video Processing")
            self.sampling_interval = st.slider(
                "Frame Sampling Interval", 
                min_value=1, 
                max_value=5, 
                value=2,
                help="Select how frequently frames are captured"
            )
            
            st.markdown("### AI Enhancements")
            col1, col2 = st.columns(2)
            with col1:
                self.ai_insights = st.toggle("AI Insights", value=True)
            with col2:
                self.sentiment_analysis = st.toggle("Sentiment", value=True)
            
            # Advanced Configuration Section
            with st.expander("🔧 Advanced Options"):
                self.detail_level = st.select_slider(
                    "Detail Extraction Level",
                    options=["Low", "Medium", "High", "Ultra"],
                    value="Medium"
                )
                st.caption("Higher levels provide more comprehensive analysis")
    
    def process_video(self, uploaded_file):
        """
        Advanced video processing with richer metadata
        """
        start_time = datetime.now()
        
        # Enhanced video processing
        processed_frames = self.video_processor.process_video(
            uploaded_file, 
            interval=self.sampling_interval,
            detail_level=self.detail_level
        )
        
        # Optional AI processing
        if self.ai_insights:
            ai_enhanced_data = self.ai_processor.process(
                processed_frames, 
                sentiment_analysis=self.sentiment_analysis
            )
            
            # Performance tracking
            end_time = datetime.now()
            ai_enhanced_data['processing_time'] = (end_time - start_time).total_seconds()
            
            return ai_enhanced_data
        
        return processed_frames
    
    def render_results(self, results: List[Dict[str, Any]]):
        """
        Create a comprehensive, visually rich results dashboard
        """
        # Performance and Overview Section
        st.markdown("## 📊 Analysis Dashboard")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🕒 Processing Time", f"{results.get('processing_time', 0):.2f} sec")
        with col2:
            st.metric("🖼️ Frames Analyzed", len(results.get('frames', [])))
        with col3:
            st.metric("📈 Complexity", results.get('detail_level', 'Medium'))
        
        # Sentiment Distribution
        if self.sentiment_analysis:
            sentiments = results.get('sentiment_distribution', {})
            
            st.markdown("### 😊 Sentiment Analysis")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig_sentiment = px.pie(
                    values=list(sentiments.values()), 
                    names=list(sentiments.keys()),
                    title="Video Content Sentiment Breakdown",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                st.plotly_chart(fig_sentiment, use_container_width=True)
            
            with col2:
                for sentiment, value in sentiments.items():
                    st.metric(sentiment, f"{value:.1%}")
        
        # Key Frame Insights
        st.markdown("### 🔍 Frame Insights")
        
        # Scrollable frame gallery
        frame_container = st.container()
        with frame_container:
            cols = st.columns(5)
            for i, frame in enumerate(results.get('frames', [])[:5]):
                with cols[i]:
                    with st.expander(f"Frame {i+1}"):
                        st.image(frame['frame_path'], use_column_width=True)
                        st.write(f"**Insight:** {frame.get('ai_insights', 'N/A')}")
                        st.write(f"**Sentiment:** {frame.get('sentiment', 'Neutral')}")
        
        # Optional Detailed Breakdown
        if self.detail_level in ['High', 'Ultra']:
            with st.expander("📜 Comprehensive Analysis"):
                st.json(results)
    
    def run(self):
        """
        Main application runner with enhanced UI
        """
        st.title("🤖 EduVision: AI-Powered Video Analysis")
        st.markdown("Unlock deep insights from your educational videos with advanced AI technology.")
        
        # Sidebar configuration
        self.render_sidebar()
        
        # Stylized file uploader
        st.markdown("### 📤 Upload Your Video")
        uploaded_file = st.file_uploader(
            "Drag and drop or click to select", 
            type=['mp4', 'avi', 'mov'],
            help="Support for MP4, AVI, and MOV formats"
        )
        
        if uploaded_file is not None:
            with st.spinner("🧠 AI is analyzing your video..."):
                results = self.process_video(uploaded_file)
            
            self.render_results(results)

def main():
    app = EnhancedStreamlitApp()
    app.run()

if __name__ == "__main__":
    main()

# streamlit run streamlit.py