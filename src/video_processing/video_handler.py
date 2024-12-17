import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import cv2
import numpy as np
from typing import List, Dict, Any
import pytesseract
from PIL import Image
from abc import ABC, abstractmethod

from src.core.base_processor import BaseProcessor
from src.core.config_manager import ConfigManager
from src.ai_integration.text_enrichment import TextEnrichmentProcessor

class VideoProcessor(BaseProcessor):
    """
    Advanced video processing with frame extraction and OCR
    """
    def __init__(self, config_manager: ConfigManager):
        super().__init__(config_manager)

        # Text enrichment processor
        self.text_enrichment = TextEnrichmentProcessor()

        # Configuration
        self.max_file_size = self.config.get_config('app', 'video_processing.max_file_size', 1073741824)
        self.allowed_extensions = self.config.get_config('app', 'video_processing.allowed_extensions', ['mp4', 'avi', 'mov'])

    def _validate_video(self, uploaded_file):
        """
        Validate uploaded video file
        
        Args:
            uploaded_file: Uploaded video file
        
        Raises:
            ValueError: If file is invalid
        """
        # Check file size
        if uploaded_file.size > self.max_file_size:
            raise ValueError(f"File size exceeds the maximum allowed size of {self.max_file_size / 1024 / 1024} bytes")
        
        # Check file extension
        file_extension = uploaded_file.name.split('.')[-1].lower()
        if file_extension not in self.allowed_extensions:
            raise ValueError(f"Invalid file extension. Allowed extensions are: {', '.join(self.allowed_extensions)}")
        
    def _extract_frames(self, video_path: str, interval: int = 2) -> List[Dict[str, Any]]:
        """
        Extract frames from video at specified intervals
        
        Args:
            video_path (str): Path to video file
            interval (int): Frame extraction interval in seconds
        
        Returns:
            List[Dict[str, Any]]: Extracted frames with metadata
        """
        frames_data = []
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Extract frame at specified interval
            if frame_count % int(fps * interval) == 0:
                # Save frame
                frame_filename = f'logs/frame_{frame_count}.jpg'
                cv2.imwrite(frame_filename, frame)

                # Perform OCR
                ocr_text = self._perform_ocr(frame_filename)

                # Enrich text
                text_enrichment = self.text_enrichment.enrich_text(ocr_text) if ocr_text else {}

                frames_data.append({
                    'frame_path': frame_filename,
                    'timestamp': frame_count / fps,
                    'text': ocr_text,
                    'text_enrichment': text_enrichment
                })
            
            frame_count += 1
        
        cap.release()
        return frames_data
    
    def _perform_ocr(self, frame_path: str) -> str:
        """
        Perform Optical Character Recognition on frame
        
        Args:
            frame_path (str): Path to frame image
        
        Returns:
            str: Extracted text
        """
        try:
            # Use Pillow for image processing
            img = Image.open(frame_path)

            # Convert to grayscale for OCR
            img_gray = img.convert('L')

            # Perform OCR
            text = pytesseract.image_to_string(img_gray, lang='eng')

            return text.strip()
        
        except Exception as e:
            self.log_error(f"OCR processing error: {e}")
            return ""
        
    def process(self, input_data, **kwargs):
        return self.process_video(input_data, **kwargs)
    
    def process_video(self, uploaded_file, interval: int = 2, detail_level='Medium') -> List[Dict[str, Any]]:
        """
        Main video processing method
        
        Args:
            uploaded_file: Uploaded video file
            interval (int): Frame extraction interval
        
        Returns:
            List[Dict[str, Any]]: Processed video frames
        """
        # Validate video
        self._validate_video(uploaded_file)

        # Save uploaded file temporarily
        temp_video_path = 'logs/uploaded_video.mp4'
        with open(temp_video_path, 'wb') as f:
            f.write(uploaded_file.read())

        try:
            # Extract and process frames
            frames_data = self._extract_frames(temp_video_path, interval)
            return frames_data
        
        except Exception as e:
            self.log_error(f"Video processing error: {e}")
            return []
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_video_path):
                os.remove(temp_video_path)