# proj/src/video_processing/video_compressor.py

# import os
# import logging
# import pathlib
# import subprocess
# from typing import Optional, Dict, Any

# class VideoCompressor:
#     @staticmethod
#     def find_ffmpeg() -> Optional[str]:
#         """Find FFmpeg executable path on Windows"""
#         ffmpeg_path = r"C:\Users\mannu\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1-full_build\bin\ffmpeg.exe"
        
#         if os.path.isfile(ffmpeg_path):
#             return ffmpeg_path
#         return None

#     @staticmethod
#     def probe_video(ffmpeg_path: str, video_path: str) -> Dict[str, Any]:
#         """Get video metadata using ffprobe"""
#         ffprobe_path = ffmpeg_path.replace('ffmpeg.exe', 'ffprobe.exe')
        
#         cmd = [
#             ffprobe_path,
#             '-v', 'error',
#             '-select_streams', 'v:0',
#             '-show_entries', 'stream=width,height,codec_name,duration',
#             '-show_entries', 'format=duration',
#             '-of', 'json',
#             str(video_path)
#         ]
        
#         try:
#             result = subprocess.run(cmd, capture_output=True, text=True, check=True)
#             import json
#             return json.loads(result.stdout)
#         except subprocess.CalledProcessError as e:
#             print(f"FFprobe error: {e.stderr}")
#             raise

#     @staticmethod
#     def list_sample_folder_contents():
#         """List contents of the sample folder with detailed path information"""
#         try:
#             script_path = pathlib.Path(__file__).resolve()
#             print(f"\nScript location: {script_path}")
            
#             project_root = script_path.parents[2]
#             print(f"Project root: {project_root}")
            
#             sample_folder = project_root / 'src' / 'video_processing' / 'sample'
#             print(f"Sample folder path: {sample_folder}")
            
#             sample_folder.mkdir(parents=True, exist_ok=True)
            
#             print("\nDirectory contents:")
#             for item in sample_folder.iterdir():
#                 size = item.stat().st_size / 1024  # KB
#                 print(f"- {item.name} (Size: {size:.2f} KB)")
#                 print(f"  Absolute path: {item.absolute()}")
#                 print(f"  Exists: {item.exists()}")
#                 print(f"  Is file: {item.is_file()}")
#                 print(f"  Read permission: {os.access(str(item), os.R_OK)}")
                
#         except Exception as e:
#             print(f"Error during path checking: {e}")
#             raise
    
#     @classmethod
#     def compress_video(
#         cls,
#         input_path: str, 
#         target_size_kb: int = 1024,
#         two_pass: bool = True,
#         filename_suffix: str = 'compressed'
#     ) -> str:
#         """Compress video using FFmpeg subprocess"""
#         try:
#             # Find FFmpeg
#             ffmpeg_path = cls.find_ffmpeg()
#             if not ffmpeg_path:
#                 raise FileNotFoundError("FFmpeg executable not found")
#             print(f"Found FFmpeg at: {ffmpeg_path}")
            
#             # Convert input path to Path object
#             video_path = pathlib.Path(input_path).resolve()
#             print(f"\nProcessing video:")
#             print(f"Input path: {video_path}")
#             print(f"Exists: {video_path.exists()}")
#             print(f"Is file: {video_path.is_file()}")
#             print(f"Read permission: {os.access(str(video_path), os.R_OK)}")

#             if not video_path.exists():
#                 raise FileNotFoundError(f"Video file not found: {video_path}")
            
#             if not video_path.is_file():
#                 raise ValueError(f"Path is not a file: {video_path}")
            
#             if not os.access(str(video_path), os.R_OK):
#                 raise PermissionError(f"No read permission for file: {video_path}")

#             # Create output path
#             output_path = video_path.parent / f"{video_path.stem}_{filename_suffix}{video_path.suffix}"
#             print(f"Output path will be: {output_path}")

#             # Ensure output directory exists
#             output_path.parent.mkdir(parents=True, exist_ok=True)

#             # Get video info
#             try:
#                 probe_data = cls.probe_video(ffmpeg_path, str(video_path))
#                 stream_data = probe_data.get('streams', [{}])[0]
#                 format_data = probe_data.get('format', {})
                
#                 duration = float(format_data.get('duration', 0))
#                 width = stream_data.get('width', '?')
#                 height = stream_data.get('height', '?')
#                 codec = stream_data.get('codec_name', 'unknown')
                
#                 print(f"\nVideo Information:")
#                 print(f"Duration: {duration:.2f} seconds")
#                 print(f"Codec: {codec}")
#                 print(f"Resolution: {width}x{height}")
                
#                 # Calculate target bitrate (bits per second)
#                 target_size_bits = target_size_kb * 8 * 1024  # Convert KB to bits
#                 bitrate = int(target_size_bits / duration)
                
#                 # Prepare FFmpeg command
#                 cmd = [
#                     ffmpeg_path,
#                     '-y',  # Overwrite output file if it exists
#                     '-i', str(video_path),
#                     '-c:v', 'libx264',
#                     '-b:v', f'{bitrate}',
#                     '-maxrate', f'{bitrate*1.5}',
#                     '-bufsize', f'{bitrate*2}',
#                     '-preset', 'medium',
#                     '-c:a', 'aac',
#                     '-b:a', '128k',
#                     str(output_path)
#                 ]
                
#                 print("\nStarting compression...")
#                 print(f"Target bitrate: {bitrate/1024/1024:.2f} Mbps")
                
#                 # Run FFmpeg
#                 result = subprocess.run(cmd, capture_output=True, text=True)
                
#                 if result.returncode != 0:
#                     print(f"FFmpeg error: {result.stderr}")
#                     raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)
                
#                 if output_path.exists():
#                     final_size = output_path.stat().st_size / 1024  # KB
#                     print(f"\nCompression complete!")
#                     print(f"Final size: {final_size:.2f} KB")
#                     return str(output_path)
#                 else:
#                     raise RuntimeError("Output file was not created")
                
#             except subprocess.CalledProcessError as e:
#                 print(f"FFmpeg process error: {e.stderr}")
#                 raise
#             except Exception as e:
#                 print(f"Error during video processing: {e}")
#                 raise

#         except Exception as e:
#             print(f"Error: {str(e)}")
#             print(f"Error type: {type(e).__name__}")
#             return False

# # Configure logging
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )


# if __name__ == "__main__":
#     try:
#         # First list contents and check paths
#         print("Checking sample folder contents...")
#         VideoCompressor.list_sample_folder_contents()
        
#         video_path = r"C:\Users\mannu\Downloads\JSproj\megaProj\vid_pro_tool\src\video_processing\sample\Transformers.mkv"
        
#         print("\nAttempting video compression...")
#         result = VideoCompressor.compress_video(video_path, target_size_kb=500000)  # 500MB target
        
#         if result:
#             print(f"Success! Compressed video saved to: {result}")
#         else:
#             print("Video compression failed")
            
#     except Exception as e:
#         print(f"Main execution error: {e}")
#         raise

##################################################################
import os
import logging
import pathlib
import subprocess
import multiprocessing
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime
from multiprocessing import Pool

class BatchVideoCompressor:
    def __init__(self, num_processes: int = None):
        self.num_processes = num_processes or max(1, multiprocessing.cpu_count() - 1)

    @staticmethod
    def find_ffmpeg() -> Optional[str]:
        """Find FFmpeg executable path on Windows"""
        ffmpeg_path = r"C:\Users\mannu\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1-full_build\bin\ffmpeg.exe"
        if os.path.isfile(ffmpeg_path):
            return ffmpeg_path
        return None

    @staticmethod
    def probe_video(ffmpeg_path: str, video_path: str) -> Dict[str, Any]:
        """Get video metadata using ffprobe"""
        ffprobe_path = ffmpeg_path.replace('ffmpeg.exe', 'ffprobe.exe')
        cmd = [
            ffprobe_path,
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height,codec_name,duration',
            '-show_entries', 'format=duration',
            '-of', 'json',
            str(video_path)
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            import json
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            logging.error(f"FFprobe error: {e.stderr}")
            raise

    @staticmethod
    def compress_video_worker(task: Tuple[int, str, int]) -> Dict[str, Any]:
        """Worker function for video compression"""
        index, video_path, target_size_kb = task
        try:
            ffmpeg_path = BatchVideoCompressor.find_ffmpeg()
            if not ffmpeg_path:
                raise FileNotFoundError("FFmpeg executable not found")

            video_path = pathlib.Path(video_path).resolve()
            output_path = video_path.parent / f"{video_path.stem}_compressed{video_path.suffix}"

            probe_data = BatchVideoCompressor.probe_video(ffmpeg_path, str(video_path))
            stream_data = probe_data.get('streams', [{}])[0]
            format_data = probe_data.get('format', {})
            
            duration = float(format_data.get('duration', 0))
            target_size_bits = target_size_kb * 8 * 1024
            bitrate = int(target_size_bits / duration)

            cmd = [
                ffmpeg_path,
                '-y',
                '-i', str(video_path),
                '-c:v', 'libx264',
                '-b:v', f'{bitrate}',
                '-maxrate', f'{bitrate*1.5}',
                '-bufsize', f'{bitrate*2}',
                '-preset', 'medium',
                '-c:a', 'aac',
                '-b:a', '128k',
                str(output_path)
            ]

            start_time = datetime.now()
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            # Monitor progress
            while process.poll() is None:
                if process.stderr:
                    line = process.stderr.readline()
                    if "time=" in line:
                        # Print progress directly
                        print(f"\rProcessing {video_path.name}: {line.strip()}", end='', flush=True)

            process.wait()
            end_time = datetime.now()

            if process.returncode == 0 and output_path.exists():
                final_size = output_path.stat().st_size / 1024
                processing_time = (end_time - start_time).total_seconds()
                
                print(f"\nCompleted {video_path.name}")
                
                return {
                    'index': index,
                    'input_path': str(video_path),
                    'output_path': str(output_path),
                    'success': True,
                    'final_size': final_size,
                    'processing_time': processing_time
                }
            else:
                error_message = process.stderr.read() if process.stderr else "Unknown error"
                raise RuntimeError(f"FFmpeg failed with return code {process.returncode}: {error_message}")

        except Exception as e:
            logging.error(f"Error processing {video_path}: {str(e)}")
            return {
                'index': index,
                'input_path': str(video_path),
                'success': False,
                'error': str(e)
            }

    def process_videos(self, video_paths: List[str], target_size_kb: int = 500000) -> List[Dict[str, Any]]:
        """Process multiple videos in parallel while maintaining order"""
        tasks = [(i, path, target_size_kb) for i, path in enumerate(video_paths)]
        
        # Process videos in parallel
        with Pool(processes=self.num_processes) as pool:
            results = pool.map(self.compress_video_worker, tasks)
        
        # Sort results by index to maintain order
        return sorted(results, key=lambda x: x['index'])

def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Sample folder path
    sample_folder = pathlib.Path(r"C:\Users\mannu\Downloads\JSproj\megaProj\vid_pro_tool\src\video_processing\sample")
    
    # Get all video files
    video_extensions = {'.mp4', '.mkv', '.avi', '.mov'}
    video_paths = [
        str(f) for f in sample_folder.iterdir()
        if f.suffix.lower() in video_extensions
    ]

    if not video_paths:
        logging.error("No video files found in the sample folder")
        return

    # Initialize batch processor
    processor = BatchVideoCompressor()
    
    # Process videos
    try:
        logging.info(f"Starting batch processing of {len(video_paths)} videos...")
        results = processor.process_videos(video_paths)
        
        # Display results summary
        print("\n\nProcessing Results:")
        print("-" * 80)
        for result in results:
            if result['success']:
                print(f"\nFile: {os.path.basename(result['input_path'])}")
                print(f"Status: Success")
                print(f"Output: {os.path.basename(result['output_path'])}")
                print(f"Final size: {result['final_size']:.2f} KB")
                print(f"Processing time: {result['processing_time']:.2f} seconds")
            else:
                print(f"\nFile: {os.path.basename(result['input_path'])}")
                print(f"Status: Failed")
                print(f"Error: {result['error']}")
                
    except Exception as e:
        logging.error(f"Batch processing error: {e}")
        raise

if __name__ == "__main__":
    main()
# python src/video_processing/video_compressor.py