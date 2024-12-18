# proj/src/video_processing/video_compressor.py

import os
import subprocess
import logging
from typing import Optional

class VideoCompressor:
    @staticmethod
    def compress_video(
        input_path: str,
        output_path: Optional[str] = None,
        target_size_mb: int = 100,
        crf: int = 23,
        preset: str = 'medium'
    ):
        """
        Compress video using FFmpeg with configurable settings.
        
        Args:
            input_path (str): Path to the input video file
            output_path (str, optional): Path for compressed video. 
                                         Defaults to input directory if not specified.
            target_size_mb (int): Target maximum file size in megabytes
            crf (int): Constant Rate Factor for quality (0-51, lower is higher quality)
            preset (str): FFmpeg compression preset (ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow)
        
        Returns:
            str: Path to the compressed video file
        """
        try:
            # if no output path specified, create one in the same directory
            if not output_path:
                base_name = os.path.splitext(input_path)[0]
                output_path = f"{base_name}_compressed.mp4"

            # FFmpeg command for compression
            ffmpeg_command = [
                'ffmpeg',
                '-i', input_path,
                '-c:v', 'libx264',  # Use libx264 codec
                '-crf', str(crf),   # Constant Rate Factor
                '-preset', preset,  # Compression preset
                'acodec', 'aac',
                output_path
            ]

            # Execute compression
            result = subprocess.run(
                ffmpeg_command,
                capture_output=True,
                text=True,
            )

            # Check if compression was successful
            if result.returncode != 0:
                logging.error(f"Video compression failed: {result.stderr}")
                raise RuntimeError("Video compression failed")
            
            # Verify compressed file size
            compressed_size = os.path.getsize(output_path) / (1024 * 1024)  # Size in MB
            if compressed_size > target_size_mb:
                logging.warning(f"Compressed file size ({compressed_size:.2f}MB) exceeds target size ({target_size_mb}MB)")
                raise RuntimeError("Compressed file size exceeds target size")
            
            return output_path
        
        except Exception as e:
            logging.error(f"Error during video compression: {e}")
            raise

    @staticmethod
    def decompress_video(
        compressed_path: str,
        output_path: Optional[str] = None
    ) -> str:
        """
        Decompress or copy back the original video.
        In this implementation, it's essentially a file copy.
        
        Args:
            compressed_path (str): Path to the compressed video
            output_path (str, optional): Destination path for decompressed video
        
        Returns:
            str: Path to the decompressed/original video file
        """
        try:
            # If no output path specified, create one in the same directory
            if not output_path:
                base_name = os.path.splitext(compressed_path)[0]
                output_path = f"{base_name}_decompressed.mp4"

            # Simply copy the file (in most cases, FFmpeg compression is reversible)
            subprocess.run(['cp', compressed_path, output_path], check=True)
            
            return output_path
        
        except Exception as e:
            logging.error(f"Error during video decompression: {e}")
            raise

# Example usage
if __name__ == "__main__":
    input_video = r"sample/Transformers.mkv"
    compressed_video = VideoCompressor.compress_video(input_video)
    print(f"Video compressed to: {compressed_video}")

# python src/video_processing/video_compressor.py
