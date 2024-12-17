# proj/src/api/chunk_api.py

import os
import uuid
import aiofiles
from fastapi import (
    FastAPI, 
    File, 
    UploadFile, 
    HTTPException, 
    Form,
    APIRouter
)
from fastapi.responses import JSONResponse
from typing import Optional

class ChunkedUploadManager:
    """
    Manages chunked file uploads with robust error handling and storage
    """
    def __init__(self, base_upload_dir: str = 'uploads/chunks'):
        """
        Initialize the chunked upload manager
        
        Args:
            base_upload_dir (str): Base directory for storing chunked uploads
        """
        self.base_upload_dir = base_upload_dir
        os.makedirs(self.base_upload_dir, exist_ok=True)

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
            upload_dir = os.path.join(self.base_upload_dir, upload_id)
            os.makedirs(upload_dir, exist_ok=True)

            # Generate chunk filename
            chunk_filename = f'chunk_{chunk_number:04d}'
            chunk_path = os.path.join(upload_dir, chunk_filename)

            # Save chunk
            async with aiofiles.open(chunk_path, 'wb') as chunk_file:
                content = await file.read()
                await chunk_file.write(content)

            # Check if all chunks are uploaded
            uploaded_chunks = len([f for f in os.listdir(upload_dir) if f.startswith('chunk_')])
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

    def assemble_chunks(self, upload_id: str, target_dir: str = 'uploads/videos') -> str:
        """
        Assemble uploaded chunks into a complete file
        
        Args:
            upload_id (str): Unique upload identifier
            target_dir (str): Directory to save the assembled file
        
        Returns:
            str: Path to the assembled file
        """
        try:
            # Ensure target directory exists
            os.makedirs(target_dir, exist_ok=True)

            # Get chunk directory
            chunk_dir = os.path.join(self.base_upload_dir, upload_id)
            
            # Verify all chunks are present
            chunks = sorted(
                [f for f in os.listdir(chunk_dir) if f.startswith('chunk_')], 
                key=lambda x: int(x.split('_')[1])
            )

            if not chunks:
                raise ValueError("No chunks found for the given upload_id")

            # Create output file path
            output_filename = f'{upload_id}.mp4'
            output_path = os.path.join(target_dir, output_filename)

            # Assemble chunks
            with open(output_path, 'wb') as outfile:
                for chunk_name in chunks:
                    chunk_path = os.path.join(chunk_dir, chunk_name)
                    with open(chunk_path, 'rb') as chunk_file:
                        outfile.write(chunk_file.read())

            return output_path

        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Chunk assembly failed: {str(e)}"
            )

def create_chunk_router() -> APIRouter:
    """
    Create a FastAPI router for chunked uploads
    
    Returns:
        APIRouter: Configured router for chunked uploads
    """
    router = APIRouter()
    upload_manager = ChunkedUploadManager()

    @router.post("/upload_chunked")
    async def upload_chunk(
        file: UploadFile = File(...),
        chunk_number: int = Form(1),
        total_chunks: int = Form(1),
        upload_id: Optional[str] = Form(None)
    ):
        """
        Handle individual chunk uploads
        
        Args:
            file (UploadFile): Uploaded file chunk
            chunk_number (int): Current chunk number
            total_chunks (int): Total number of chunks
            upload_id (str, optional): Unique upload identifier
        
        Returns:
            JSONResponse: Upload status and metadata
        """
        # Generate upload ID if not provided
        upload_id = upload_id or str(uuid.uuid4())

        # Save the chunk
        result = await upload_manager.save_chunk(
            file, upload_id, chunk_number, total_chunks
        )

        # If all chunks are uploaded, assemble the file
        if result['status'] == 'completed':
            assembled_file_path = upload_manager.assemble_chunks(upload_id)
            result['file_path'] = assembled_file_path

        return JSONResponse(content=result)

    @router.get("/check_upload/{upload_id}")
    async def check_upload_status(upload_id: str):
        """
        Check the status of a chunked upload
        
        Args:
            upload_id (str): Unique upload identifier
        
        Returns:
            JSONResponse: Upload status details
        """
        try:
            chunk_dir = os.path.join('uploads/chunks', upload_id)
            
            # Check if upload directory exists
            if not os.path.exists(chunk_dir):
                return JSONResponse({
                    'status': 'not_found',
                    'message': 'No upload found with this ID'
                }, status_code=404)

            # Count uploaded chunks
            chunks = [f for f in os.listdir(chunk_dir) if f.startswith('chunk_')]
            
            return JSONResponse({
                'status': 'in_progress',
                'upload_id': upload_id,
                'chunks_uploaded': len(chunks)
            })

        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error checking upload status: {str(e)}"
            )

    return router

def include_chunk_router(app: FastAPI):
    """
    Include the chunked upload router in the main FastAPI application
    
    Args:
        app (FastAPI): Main FastAPI application
    """
    chunk_router = create_chunk_router()
    app.include_router(chunk_router, prefix="/chunk", tags=["Chunked Uploads"])