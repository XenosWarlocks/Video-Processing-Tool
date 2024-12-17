# proj/src/api/vid_api.py

import json
import os
import uuid
import aiofiles
from fastapi import (
    FastAPI, 
    File, 
    UploadFile, 
    HTTPException, 
    BackgroundTasks
)
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

from src.video_processing.video_handler import VideoProcessor
from src.ai_integration.gemini_processor import GeminiProcessor
from src.core.config_manager import ConfigManager

class ChunkedUploadResponse(BaseModel):
    upload_id: str
    status: str
    total_chunks_expected: int

class VideoProcessingRequest(BaseModel):
    upload_id: str
    processing_options: Optional[List[str]] = None

class VideoProcessingAPI:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.video_processor = VideoProcessor(self.config_manager)
        self.ai_processor = GeminiProcessor(self.config_manager)
        
        # Create upload and temp directories
        os.makedirs('uploads/chunks', exist_ok=True)
        os.makedirs('uploads/videos', exist_ok=True)
        os.makedirs('uploads/processed', exist_ok=True)
    
    async def handle_chunked_upload(
        self, 
        file: UploadFile, 
        chunk_number: int, 
        total_chunks: int, 
        upload_id: str
    ):
        """
        Handle chunked video file upload
        
        Args:
            file (UploadFile): Uploaded file chunk
            chunk_number (int): Current chunk number
            total_chunks (int): Total number of chunks
            upload_id (str): Unique upload identifier
        """
        chunk_dir = os.path.join('uploads/chunks', upload_id)
        os.makedirs(chunk_dir, exist_ok=True)
        
        chunk_path = os.path.join(chunk_dir, f'chunk_{chunk_number:04d}')
        
        async with aiofiles.open(chunk_path, 'wb') as chunk_file:
            content = await file.read()
            await chunk_file.write(content)
    
    def assemble_video_from_chunks(self, upload_id: str) -> str:
        """
        Assemble video from uploaded chunks
        
        Args:
            upload_id (str): Unique upload identifier
        
        Returns:
            str: Path to the assembled video file
        """
        chunk_dir = os.path.join('uploads/chunks', upload_id)
        video_path = os.path.join('uploads/videos', f'{upload_id}.mp4')
        
        # Sort chunks and concatenate
        chunks = sorted(
            [f for f in os.listdir(chunk_dir) if f.startswith('chunk_')], 
            key=lambda x: int(x.split('_')[1])
        )
        
        with open(video_path, 'wb') as outfile:
            for chunk_name in chunks:
                chunk_path = os.path.join(chunk_dir, chunk_name)
                with open(chunk_path, 'rb') as chunk_file:
                    outfile.write(chunk_file.read())
        
        return video_path
    
    async def process_video_background(
        self, 
        video_path: str, 
        processing_options: Optional[List[str]] = None
    ):
        """
        Background task for video processing
        
        Args:
            video_path (str): Path to the video file
            processing_options (List[str], optional): Processing configurations
        """
        try:
            # Process video
            processed_frames = self.video_processor.process_video(
                video_path, 
                interval=2  # Default 2-second interval
            )
            
            # Optional AI processing
            if processing_options and 'ai_insights' in processing_options:
                ai_results = self.ai_processor.process(processed_frames)
                
                # Save results to a file or database
                self._save_processing_results(video_path, ai_results)
        
        except Exception as e:
            # Log processing errors
            print(f"Video processing error: {e}")
    
    def _save_processing_results(self, video_path: str, results: List[dict]):
        """
        Save processing results
        
        Args:
            video_path (str): Original video path
            results (List[dict]): Processing results
        """
        # Create a unique filename for results
        result_filename = os.path.join(
            'uploads/processed', 
            f'{os.path.basename(video_path)}_results.json'
        )
        
        # Save results as JSON
        with open(result_filename, 'w') as f:
            json.dump(results, f, indent=2)

def create_app() -> FastAPI:
    """
    Create FastAPI application
    
    Returns:
        FastAPI: Configured FastAPI application
    """
    app = FastAPI(
        title="Educational Video Processing API",
        description="Robust video processing API with chunked uploads and AI insights"
    )
    video_api = VideoProcessingAPI()

    @app.post("/upload/chunked")
    async def upload_chunked_video(
        file: UploadFile = File(...),
        chunk_number: int = 1,
        total_chunks: int = 1,
        upload_id: Optional[str] = None
    ):
        """
        Handle chunked video file upload
        
        Args:
            file (UploadFile): Uploaded file chunk
            chunk_number (int): Current chunk number
            total_chunks (int): Total number of chunks
            upload_id (str, optional): Unique upload identifier
        
        Returns:
            ChunkedUploadResponse: Upload status response
        """
        if not upload_id:
            upload_id = str(uuid.uuid4())
        
        try:
            await video_api.handle_chunked_upload(
                file, chunk_number, total_chunks, upload_id
            )
            
            # If last chunk, assemble video
            if chunk_number == total_chunks:
                video_path = video_api.assemble_video_from_chunks(upload_id)
                return ChunkedUploadResponse(
                    upload_id=upload_id,
                    status='completed',
                    total_chunks_expected=total_chunks
                )
            
            return ChunkedUploadResponse(
                upload_id=upload_id,
                status='partial',
                total_chunks_expected=total_chunks
            )
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/process")
    async def process_video(
        request: VideoProcessingRequest,
        background_tasks: BackgroundTasks
    ):
        """
        Start video processing
        
        Args:
            request (VideoProcessingRequest): Processing request
            background_tasks (BackgroundTasks): FastAPI background tasks
        
        Returns:
            JSONResponse: Processing initiation response
        """
        try:
            # Locate video path
            chunk_dir = os.path.join('uploads/chunks', request.upload_id)
            video_path = video_api.assemble_video_from_chunks(request.upload_id)
            
            # Start background processing
            background_tasks.add_task(
                video_api.process_video_background, 
                video_path, 
                request.processing_options
            )
            
            return JSONResponse({
                'status': 'processing_started',
                'upload_id': request.upload_id
            })
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return app

app = create_app()