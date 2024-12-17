# proj/src/video_processing/frame_.py

import cv2
import numpy as np
from typing import List, Dict, Any, Optional
import os
from skimage.metrics import structural_similarity as ssim

class AdvancedFrameExtractor:
    """
    Advanced frame extraction with intelligent sampling and filtering
    """
    def __init__(
        self, 
        interval: int = 2, 
        min_frame_difference: float = 0.3,
        max_frames: int = 50
    ):
        """
        Initialize frame extractor
        
        Args:
            interval (int): Base frame extraction interval
            min_frame_difference (float): Minimum similarity threshold
            max_frames (int): Maximum number of frames to extract
        """
        self.interval = interval
        self.min_frame_difference = min_frame_difference
        self.max_frames = max_frames
    
    def extract_keyframes(self, video_path: str) -> List[Dict[str, Any]]:
        """
        Extract keyframes using advanced filtering techniques
        
        Args:
            video_path (str): Path to video file
        
        Returns:
            List[Dict[str, Any]]: Extracted keyframes with metadata
        """
        cap = cv2.VideoCapture(video_path)
        
        # Video metadata
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        keyframes = []
        last_keyframe = None
        frame_count = 0
        
        while frame_count < total_frames and len(keyframes) < self.max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Sample frames based on interval
            if frame_count % int(fps * self.interval) == 0:
                # Convert frame to grayscale for comparison
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Check frame difference
                if last_keyframe is None or self._is_significant_frame(last_keyframe, gray_frame):
                    # Save keyframe
                    keyframe_path = self._save_keyframe(frame, frame_count)
                    
                    keyframe_info = {
                        'path': keyframe_path,
                        'timestamp': frame_count / fps,
                        'frame_number': frame_count
                    }
                    
                    keyframes.append(keyframe_info)
                    last_keyframe = gray_frame
            
            frame_count += 1
        
        cap.release()
        return keyframes
    
    def _is_significant_frame(self, last_frame: np.ndarray, current_frame: np.ndarray) -> bool:
        """
        Determine if frame is significantly different
        
        Args:
            last_frame (np.ndarray): Previous keyframe
            current_frame (np.ndarray): Current frame
        
        Returns:
            bool: Whether frame is significant
        """
        # Compute structural similarity index
        similarity = ssim(last_frame, current_frame)
        
        # More complex deviation detection
        return similarity < self.min_frame_difference
    
    def _save_keyframe(self, frame: np.ndarray, frame_count: int) -> str:
        """
        Save keyframe to disk
        
        Args:
            frame (np.ndarray): Frame to save
            frame_count (int): Frame number
        
        Returns:
            str: Path to saved keyframe
        """
        # Ensure logs directory exists
        os.makedirs('logs/keyframes', exist_ok=True)
        
        # Generate unique filename
        keyframe_path = f'logs/keyframes/keyframe_{frame_count}.jpg'
        cv2.imwrite(keyframe_path, frame)
        
        return keyframe_path
    
    def analyze_scene_changes(self, video_path: str) -> List[Dict[str, Any]]:
        """
        Analyze scene changes in the video
        
        Args:
            video_path (str): Path to video file
        
        Returns:
            List[Dict[str, Any]]: Scene change information
        """
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        scene_changes = []
        prev_frame = None
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            if prev_frame is not None:
                # Compute frame difference
                frame_diff = cv2.absdiff(prev_frame, gray_frame)
                non_zero_count = np.count_nonzero(frame_diff)
                
                # Scene change detection
                if non_zero_count > (frame_diff.size * 0.1):  # 10% change threshold
                    scene_changes.append({
                        'timestamp': frame_count / fps,
                        'frame_number': frame_count,
                        'change_intensity': non_zero_count / frame_diff.size
                    })
            
            prev_frame = gray_frame
            frame_count += 1
        
        cap.release()
        return scene_changes