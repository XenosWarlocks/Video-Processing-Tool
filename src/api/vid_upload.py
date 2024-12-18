# proj/src/api/vid_upload.py

import uuid
import requests
import os
from typing import Optional

class VideoChunkUploader:
    def __init__(self, api_url: str = "http://localhost:8000"):
        """
        Initialize video chunk uploader
        
        Args:
            api_url (str): Base URL of the video processing API
        """
        self.api_url = api_url.rstrip('/')  # Remove trailing slash if present

    def upload_video_in_chunks(
        self,
        file_path: str,
        chunk_size: int = 10 * 1024 * 1024,  # 10 MB chunks
        upload_id: Optional[str] = None
    ) -> str:
        """
        Upload a video file in chunks
        
        Args:
            file_path (str): Path to the video file
            chunk_size (int): Size of each chunk
            upload_id (str, optional): Predefined upload ID
        
        Returns:
            str: Upload ID for tracking
        """
        # Validate file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Video file not found: {file_path}")

        # Get file size and calculate total chunks
        file_size = os.path.getsize(file_path)
        total_chunks = (file_size + chunk_size - 1) // chunk_size

        # Generate upload ID if not provided
        upload_id = upload_id or str(uuid.uuid4())
        
        # Chunk and upload
        with open(file_path, 'rb') as file:
            for chunk_number in range(1, total_chunks + 1):
                chunk = file.read(chunk_size)
                
                # Prepare multipart form data
                files = {
                    'file': (
                        os.path.basename(file_path),
                        chunk,
                        'application/octet-stream'
                    )
                }

                # Upload chunk with timeout and error handling
                try:
                    response = requests.post(
                        f"{self.api_url}/video/upload",
                        files=files,
                        data={
                            'chunk_number': chunk_number,
                            'total_chunks': total_chunks,
                            'upload_id': upload_id
                        },
                        timeout=30  # Set timeout to 30 seconds
                    )

                    # Raise an exception for bad status codes
                    response.raise_for_status()
                    
                except requests.RequestException as e:
                    raise Exception(f"Chunk upload failed: {e}")
                
                # # Check response
                # if response.status_code not in [200, 201]:
                #     raise Exception(f"Chunk upload failed: {response.text}")
                
        return upload_id
    
    def start_video_processing(
        self,
        upload_id: str,
        processing_options: Optional[list] = None
    ) -> dict:
        """
        Start video processing

        Args:
            upload_id (str): Unique upload identifier
            processing_options (list, optional): Processing configurations

        Returns:
            dict: Processing initiation response
        """
        
        try:
            # Prepare request payload
            response = requests.post(
                f"{self.api_url}/video/process",
                json={
                    'upload_id': upload_id,
                    'processing_options': processing_options or ['ai_insights']
                },
                timeout=120     # 2-minute timeout for processing request
            )

            # Raise an exception for bad status codes
            response.raise_for_status()

            return response.json()
        
        except requests.RequestException as e:
            raise Exception(f"Processing initiation failed: {e}")
    
# Example usage
def main():
    uploader = VideoChunkUploader()
    
    try:
        # Upload video in chunks
        video_path = 'path/to/your/video.mp4'  # Replace with actual path
        upload_id = uploader.upload_video_in_chunks(video_path)
        
        # Start processing
        processing_response = uploader.start_video_processing(
            upload_id, 
            processing_options=['ai_insights', 'sentiment_analysis']
        )
        
        print(f"Processing started: {processing_response}")
    
    except Exception as e:
        print(f"Upload/Processing error: {e}")

if __name__ == "__main__":
    main()