# proj/tests/test_video_upload.py

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
            pytest.skip("Test video file not found")
        
        return str(video_path)

    @pytest.fixture
    def test_client(self):
        """Fixture to provide FastAPI test client"""
        app = create_app()
        return TestClient(app)

    @pytest.fixture
    def uploader(self):
        """Fixture to provide VideoChunkUploader instance"""
        return VideoChunkUploader(api_url="http://testserver")

    def test_chunk_upload_and_processing(self, test_video_path, test_client, uploader):
        """Test complete flow of chunked upload and processing initiation"""
        
        # Get file size and calculate chunks
        file_size = os.path.getsize(test_video_path)
        chunk_size = 5 * 1024 * 1024  # 5MB chunks
        total_chunks = (file_size + chunk_size - 1) // chunk_size

        # Read and upload file in chunks
        with open(test_video_path, 'rb') as file:
            upload_id = None
            
            for chunk_number in range(1, total_chunks + 1):
                chunk = file.read(chunk_size)
                
                # Prepare upload data
                files = {
                    'file': ('test_vid.mp4', chunk, 'application/octet-stream')
                }
                data = {
                    'chunk_number': chunk_number,
                    'total_chunks': total_chunks,
                }
                
                if upload_id:
                    data['upload_id'] = upload_id

                # Upload chunk
                response = test_client.post(
                    "/video/upload",
                    files=files,
                    data=data
                )
                
                assert response.status_code == 200
                response_data = response.json()
                
                # Save upload_id from first chunk
                if not upload_id:
                    upload_id = response_data['upload_id']
                
                # Verify response structure
                assert 'upload_id' in response_data
                assert 'status' in response_data
                assert 'total_chunks' in response_data
                
                # Check completion status
                if chunk_number == total_chunks:
                    assert response_data['status'] == 'completed'
                else:
                    assert response_data['status'] == 'partial'

        # Test processing initiation
        processing_response = test_client.post(
            "/video/process",
            json={
                'upload_id': upload_id,
                'processing_options': ['ai_insights']
            }
        )
        
        assert processing_response.status_code == 200
        process_data = processing_response.json()
        assert process_data['status'] == 'processing_started'
        assert process_data['upload_id'] == upload_id

    @pytest.mark.asyncio
    async def test_upload_manager_methods(self, test_video_path, test_client):
        """Test individual upload manager methods"""
        from src.api.vid_api import VideoUploadManager
        
        # Initialize upload manager
        upload_manager = VideoUploadManager()
        
        # Test chunk saving
        chunk_size = 5 * 1024 * 1024
        with open(test_video_path, 'rb') as file:
            chunk = file.read(chunk_size)
            
            # Create mock UploadFile
            class MockUploadFile:
                async def read(self):
                    return chunk
                
            mock_file = MockUploadFile()
            
            # Test saving first chunk
            result = await upload_manager.save_chunk(
                mock_file,
                'test_upload_id',
                1,
                2
            )
            
            assert result['status'] == 'partial'
            assert result['chunks_uploaded'] == 1
            
            # Test saving second (final) chunk
            result = await upload_manager.save_chunk(
                mock_file,
                'test_upload_id',
                2,
                2
            )
            
            assert result['status'] == 'completed'
            assert result['chunks_uploaded'] == 2

    def test_error_handling(self, test_client):
        """Test error handling for invalid uploads"""
        
        # Test invalid chunk number
        response = test_client.post(
            "/video/upload",
            files={'file': ('test.mp4', b'dummy data', 'application/octet-stream')},
            data={'chunk_number': 0, 'total_chunks': 1}
        )
        assert response.status_code != 200
        
        # Test missing file
        response = test_client.post(
            "/video/upload",
            data={'chunk_number': 1, 'total_chunks': 1}
        )
        assert response.status_code != 200
        
        # Test invalid processing request
        response = test_client.post(
            "/video/process",
            json={'upload_id': 'invalid_id'}
        )
        assert response.status_code != 200

if __name__ == "__main__":
    pytest.main([__file__])

# pytest -v tests/test_video_upload.py