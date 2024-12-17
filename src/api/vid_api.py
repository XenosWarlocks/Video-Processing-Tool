# proj/src/api/vid_api.py
import os
import sys
import uuid
import json
import aiofiles
from typing import List, Optional

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fastapi import (
    FastAPI, 
    File, 
    UploadFile, 
    HTTPException, 
    BackgroundTasks,
    APIRouter
)
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.video_processing.video_handler import VideoProcessor
from src.ai_integration.gemini_processor import GeminiProcessor
from src.core.config_manager import ConfigManager

class ChunkedUploadResponse(BaseModel):
    upload_id: str
    status: str
    total_chunks: int

class VideoProcessingRequest(BaseModel):
    upload_id: str
    processing_options: Optional[List[str]] = None

class VideoUploadManager:
    """
    Centralized manager for video uploads and processing
    """
    def __init__(self):
        self.config_manager = ConfigManager()
        self.video_processor = VideoProcessor(self.config_manager)
        self.ai_processor = GeminiProcessor(self.config_manager)
        
        # Ensure necessary directories exist
        for dir_path in ['uploads/chunks', 'uploads/videos', 'uploads/processed']:
            os.makedirs(dir_path, exist_ok=True)

    async def save_chunk(
        self, 
        file: UploadFile, 
        upload_id: str, 
        chunk_number: int, 
        total_chunks: int
    ) -> dict:
        """
        Save an individual chunk of a file
        
        Args:
            file (UploadFile): The chunk file to save
            upload_id (str): Unique identifier for the upload
            chunk_number (int): Current chunk number
            total_chunks (int): Total number of chunks
        
        Returns:
            dict: Upload status and metadata
        """
        try:
            # Create upload-specific directory
            chunk_dir = os.path.join('uploads/chunks', upload_id)
            os.makedirs(chunk_dir, exist_ok=True)

            # Generate chunk filename
            chunk_filename = f'chunk_{chunk_number:04d}'
            chunk_path = os.path.join(chunk_dir, chunk_filename)

            # Save chunk
            async with aiofiles.open(chunk_path, 'wb') as chunk_file:
                content = await file.read()
                await chunk_file.write(content)

            # Check if all chunks are uploaded
            uploaded_chunks = len([f for f in os.listdir(chunk_dir) if f.startswith('chunk_')])
            is_complete = uploaded_chunks == total_chunks

            return {
                'upload_id': upload_id,
                'chunk_number': chunk_number,
                'total_chunks': total_chunks,
                'status': 'completed' if is_complete else 'partial',
                'chunks_uploaded': uploaded_chunks
            }

        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Chunk upload failed: {str(e)}"
            )

    def assemble_video(self, upload_id: str) -> str:
        """
        Assemble video from uploaded chunks
        
        Args:
            upload_id (str): Unique upload identifier
        
        Returns:
            str: Path to the assembled video file
        """
        chunk_dir = os.path.join('uploads/chunks', upload_id)
        video_path = os.path.join('uploads/videos', f'{upload_id}.mp4')
        
        # Sort and concatenate chunks
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

    async def process_video(
        self, 
        video_path: str, 
        processing_options: Optional[List[str]] = None
    ) -> dict:
        """
        Process video with optional AI insights
        
        Args:
            video_path (str): Path to the video file
            processing_options (List[str], optional): Processing configurations
        
        Returns:
            dict: Processing results
        """
        try:
            # Process video frames
            processed_frames = self.video_processor.process_video(
                video_path, 
                interval=2  # Default 2-second interval
            )
            
            # Optional AI processing
            results = {}
            if processing_options and 'ai_insights' in processing_options:
                results['ai_insights'] = self.ai_processor.process(processed_frames)
            
            # Save and return results
            results_path = self._save_processing_results(video_path, results)
            results['results_path'] = results_path
            
            return results

        except Exception as e:
            print(f"Video processing error: {e}")
            return {'error': str(e)}

    def _save_processing_results(self, video_path: str, results: dict) -> str:
        """
        Save processing results to a JSON file
        
        Args:
            video_path (str): Original video path
            results (dict): Processing results
        
        Returns:
            str: Path to the saved results file
        """
        result_filename = os.path.join(
            'uploads/processed', 
            f'{os.path.basename(video_path)}_results.json'
        )
        
        with open(result_filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        return result_filename

def create_video_router(upload_manager: VideoUploadManager) -> APIRouter:
    """
    Create a FastAPI router for video upload and processing
    
    Args:
        upload_manager (VideoUploadManager): Manager for video uploads
    
    Returns:
        APIRouter: Configured router for video operations
    """
    router = APIRouter(prefix="/video", tags=["Video Processing"])

    @router.post("/upload")
    async def upload_chunk(
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
        # Generate upload ID if not provided
        upload_id = upload_id or str(uuid.uuid4())
        
        try:
            # Save the chunk
            upload_result = await upload_manager.save_chunk(
                file, upload_id, chunk_number, total_chunks
            )
            
            # Assemble video if all chunks are uploaded
            if upload_result['status'] == 'completed':
                video_path = upload_manager.assemble_video(upload_id)
                upload_result['video_path'] = video_path
            
            return ChunkedUploadResponse(
                upload_id=upload_id,
                status=upload_result['status'],
                total_chunks=total_chunks
            )
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/process")
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
            # Get video path
            video_path = os.path.join('uploads/videos', f'{request.upload_id}.mp4')
            
            # Start background processing
            background_tasks.add_task(
                upload_manager.process_video, 
                video_path, 
                request.processing_options
            )
            
            return JSONResponse({
                'status': 'processing_started',
                'upload_id': request.upload_id
            })
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router

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
    
    # Create upload manager
    upload_manager = VideoUploadManager()
    
    # Include video router
    app.include_router(create_video_router(upload_manager))
    
    return app

# Create the FastAPI application
app = create_app()