# proj/src/tests/test_video_upload.py

import os
import pytest
import asyncio
from fastapi.testclient import TestClient
from pathlib import Path

# Add project root to path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.api.vid_api import create_app
from src.api.vid_upload import VideoChunkUploader

class TestVideoUpload:
    @pytest.fixture
    def test_video_path(self):
        """Fixture to provide path to test video"""
        # Get the absolute path to the test video
        test_dir = Path(__file__).parent
        video_path = test_dir / "sample" / "test_vid.mp4"

        if not video_path.exists():
            pytest.fail(f"Test video not found at {video_path}")

        return str(video_path)
# pytest -v test_video_upload.py