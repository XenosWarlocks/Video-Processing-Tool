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
# import os
# import logging
# import pathlib
# import subprocess
# import multiprocessing
# from typing import Optional, Dict, Any, List, Tuple
# from datetime import datetime
# from multiprocessing import Pool

# class BatchVideoCompressor:
#     def __init__(self, num_processes: int = None):
#         self.num_processes = num_processes or max(1, multiprocessing.cpu_count() - 1)

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
#             logging.error(f"FFprobe error: {e.stderr}")
#             raise

#     @staticmethod
#     def compress_video_worker(task: Tuple[int, str, int]) -> Dict[str, Any]:
#         """Worker function for video compression"""
#         index, video_path, target_size_kb = task
#         try:
#             ffmpeg_path = BatchVideoCompressor.find_ffmpeg()
#             if not ffmpeg_path:
#                 raise FileNotFoundError("FFmpeg executable not found")

#             video_path = pathlib.Path(video_path).resolve()
#             output_path = video_path.parent / f"{video_path.stem}_compressed{video_path.suffix}"

#             probe_data = BatchVideoCompressor.probe_video(ffmpeg_path, str(video_path))
#             stream_data = probe_data.get('streams', [{}])[0]
#             format_data = probe_data.get('format', {})
            
#             duration = float(format_data.get('duration', 0))
#             target_size_bits = target_size_kb * 8 * 1024
#             bitrate = int(target_size_bits / duration)

#             cmd = [
#                 ffmpeg_path,
#                 '-y',
#                 '-i', str(video_path),
#                 '-c:v', 'libx264',
#                 '-b:v', f'{bitrate}',
#                 '-maxrate', f'{bitrate*1.5}',
#                 '-bufsize', f'{bitrate*2}',
#                 '-preset', 'medium',
#                 '-c:a', 'aac',
#                 '-b:a', '128k',
#                 str(output_path)
#             ]

#             start_time = datetime.now()
#             process = subprocess.Popen(
#                 cmd,
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 universal_newlines=True
#             )

#             # Monitor progress
#             while process.poll() is None:
#                 if process.stderr:
#                     line = process.stderr.readline()
#                     if "time=" in line:
#                         # Print progress directly
#                         print(f"\rProcessing {video_path.name}: {line.strip()}", end='', flush=True)

#             process.wait()
#             end_time = datetime.now()

#             if process.returncode == 0 and output_path.exists():
#                 final_size = output_path.stat().st_size / 1024
#                 processing_time = (end_time - start_time).total_seconds()
                
#                 print(f"\nCompleted {video_path.name}")
                
#                 return {
#                     'index': index,
#                     'input_path': str(video_path),
#                     'output_path': str(output_path),
#                     'success': True,
#                     'final_size': final_size,
#                     'processing_time': processing_time
#                 }
#             else:
#                 error_message = process.stderr.read() if process.stderr else "Unknown error"
#                 raise RuntimeError(f"FFmpeg failed with return code {process.returncode}: {error_message}")

#         except Exception as e:
#             logging.error(f"Error processing {video_path}: {str(e)}")
#             return {
#                 'index': index,
#                 'input_path': str(video_path),
#                 'success': False,
#                 'error': str(e)
#             }

#     def process_videos(self, video_paths: List[str], target_size_kb: int = 500000) -> List[Dict[str, Any]]:
#         """Process multiple videos in parallel while maintaining order"""
#         tasks = [(i, path, target_size_kb) for i, path in enumerate(video_paths)]
        
#         # Process videos in parallel
#         with Pool(processes=self.num_processes) as pool:
#             results = pool.map(self.compress_video_worker, tasks)
        
#         # Sort results by index to maintain order
#         return sorted(results, key=lambda x: x['index'])

###################################################################
import os
import logging
import pathlib
import subprocess
import multiprocessing
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime
from multiprocessing import Pool

class BatchVideoCompressor:
    def __init__(self, num_processes: Optional[int] = None):
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
            '-show_entries', 'stream=width,height,codec_name,r_frame_rate,bit_rate',
            '-show_entries', 'format=duration,bit_rate',
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
    def calculate_target_bitrate(target_size_kb: int, duration: float, audio_bitrate: int = 128000) -> int:
        """Calculate target video bitrate based on desired file size"""
        target_size_bits = target_size_kb * 8 * 1024
        total_audio_bits = duration * audio_bitrate
        available_video_bits = target_size_bits - total_audio_bits
        video_bitrate = int(available_video_bits / duration)
        return max(video_bitrate, 100000)  # Ensure minimum bitrate of 100kbps

    @staticmethod
    def get_compression_settings(probe_data: Dict[str, Any], target_size_kb: int) -> Dict[str, Any]:
        """Determine optimal compression settings based on video properties"""
        stream_data = probe_data.get('streams', [{}])[0]
        format_data = probe_data.get('format', {})
        
        duration = float(format_data.get('duration', 0))
        original_bitrate = int(format_data.get('bit_rate', 0))
        width = int(stream_data.get('width', 0))
        height = int(stream_data.get('height', 0))

        # Calculate target bitrate
        target_bitrate = BatchVideoCompressor.calculate_target_bitrate(target_size_kb, duration)
        
        # Adjust resolution if necessary
        new_width = width
        new_height = height
        if target_bitrate < original_bitrate * 0.7:  # If significant compression needed
            scale_factor = min(1, (target_bitrate / original_bitrate) ** 0.5)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            # Ensure dimensions are even
            new_width = new_width - (new_width % 2)
            new_height = new_height - (new_height % 2)

        return {
            'target_bitrate': target_bitrate,
            'width': new_width,
            'height': new_height,
            'crf': min(28, int(23 + (original_bitrate / target_bitrate)))  # Adjust CRF based on compression ratio
        }

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

            # Get video metadata and calculate compression settings
            probe_data = BatchVideoCompressor.probe_video(ffmpeg_path, str(video_path))
            settings = BatchVideoCompressor.get_compression_settings(probe_data, target_size_kb)

            cmd = [
                ffmpeg_path,
                '-y',
                '-i', str(video_path),
                '-c:v', 'libx264',
                '-crf', str(settings['crf']),
                '-maxrate', f'{settings["target_bitrate"]}',
                '-bufsize', f'{settings["target_bitrate"]*2}',
                '-vf', f'scale={settings["width"]}:{settings["height"]}',
                '-preset', 'slower',  # Better compression at cost of speed
                '-tune', 'film',      # Optimize for movie content
                '-profile:v', 'high', # Use high profile for better compression
                '-level', '4.1',      # Maintain compatibility
                '-movflags', '+faststart',  # Enable streaming
                '-c:a', 'aac',
                '-b:a', '128k',
                str(output_path)
            ]

            start_time = datetime.now()
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False  # Don't raise an exception
            )

            while process.poll() is None:
                if process.stderr:
                    line = process.stderr.readline()
                    if "time=" in line:
                        print(f"\rProcessing {video_path.name}: {line.strip()}", end='', flush=True)

            process.wait()
            end_time = datetime.now()

            if process.returncode == 0 and output_path.exists():
                final_size = output_path.stat().st_size / 1024
                processing_time = (end_time - start_time).total_seconds()
                
                compression_ratio = (pathlib.Path(video_path).stat().st_size / 1024) / final_size
                print(f"\nCompleted {video_path.name} (Compression ratio: {compression_ratio:.2f}x)")
                
                return {
                    'index': index,
                    'input_path': str(video_path),
                    'output_path': str(output_path),
                    'success': True,
                    'final_size': final_size,
                    'processing_time': processing_time,
                    'compression_ratio': compression_ratio,
                    'settings_used': settings
                }
            else:
                error_message = process.stderr.read() if process.stderr else "Unknown error"
                if process.returncode != 0:
                    logging.error(f"FFmpeg command that failed: {' '.join(cmd)}")
                    logging.error(f"FFmpeg error output: {error_message}")
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
        
        with Pool(processes=self.num_processes) as pool:
            results = pool.map(self.compress_video_worker, tasks)
        
        return sorted(results, key=lambda x: x['index'])


def verify_ffmpeg(ffmpeg_path: str) -> bool:
    """Verify FFmpeg installation and permissions"""
    try:
        result = subprocess.run([ffmpeg_path, '-version'], 
                              capture_output=True, 
                              text=True)
        return result.returncode == 0
    except Exception as e:
        logging.error(f"FFmpeg verification failed: {e}")
        return False

def test_ffmpeg():
    ffmpeg_path = BatchVideoCompressor.find_ffmpeg()
    if not ffmpeg_path:
        print("FFmpeg not found")
        return
    
    try:
        result = subprocess.run([ffmpeg_path, '-version'], 
                              capture_output=True, 
                              text=True)
        print("FFmpeg version output:", result.stdout)
        return result.returncode == 0
    except Exception as e:
        print(f"FFmpeg test failed: {e}")
        return False

def test_video_compression(video_path):
    ffmpeg_path = BatchVideoCompressor.find_ffmpeg()
    input_path = pathlib.Path(video_path)
    output_path = input_path.parent / f"test_{input_path.name}"
    
    # Simple command with minimal parameters
    cmd = [
        ffmpeg_path,
        '-y',  # Overwrite output file
        '-i', str(input_path),
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        str(output_path)
    ]
    
    print("Testing simple compression command:")
    print(" ".join(cmd))
    
    try:
        result = subprocess.run(cmd, 
                              capture_output=True, 
                              text=True,
                              check=True)
        print("Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error output: {e.stderr}")
        return False

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Add this at the start of main():
    if not test_ffmpeg():
        print("FFmpeg is not working properly")
        return
    # Add this to main() after the FFmpeg test:
    video_path = r"C:\Users\mannu\Downloads\JSproj\megaProj\vid_pro_tool\src\video_processing\sample\Transformers.mp4"
    if not test_video_compression(video_path):
        print("Basic video compression failed")
        return

    # Verify FFmpeg installation
    ffmpeg_path = BatchVideoCompressor.find_ffmpeg()
    if not ffmpeg_path:
        logging.error("FFmpeg not found")
        return
    
    if not verify_ffmpeg(ffmpeg_path):
        logging.error("FFmpeg verification failed")
        return

    # Verify input file exists and is readable
    sample_folder = pathlib.Path(r"C:\Users\mannu\Downloads\JSproj\megaProj\vid_pro_tool\src\video_processing\sample")
    if not sample_folder.exists():
        logging.error(f"Sample folder not found: {sample_folder}")
        return

    # Get all video files and verify they exist
    video_extensions = {'.mp4', '.mkv', '.avi', '.mov'}
    video_paths = []
    for f in sample_folder.iterdir():
        if f.suffix.lower() in video_extensions:
            if not f.is_file():
                logging.error(f"Not a file: {f}")
                continue
            try:
                with open(f, 'rb') as test:
                    pass
                video_paths.append(str(f))
            except PermissionError:
                logging.error(f"Permission denied: {f}")
            except Exception as e:
                logging.error(f"Error accessing {f}: {e}")

    if not video_paths:
        logging.error("No accessible video files found in the sample folder")
        return

    # Initialize batch processor
    processor = BatchVideoCompressor()
    
    # Process videos with lower target size for testing
    try:
        logging.info(f"Starting batch processing of {len(video_paths)} videos...")
        # Start with a smaller test compression
        results = processor.process_videos(video_paths, target_size_kb=100000)  # Try with 100MB first
        
        print("\n\nProcessing Results:")
        print("-" * 80)
        for result in results:
            if result['success']:
                print(f"\nFile: {os.path.basename(result['input_path'])}")
                print(f"Status: Success")
                print(f"Output: {os.path.basename(result['output_path'])}")
                print(f"Final size: {result['final_size']:.2f} KB")
                print(f"Processing time: {result['processing_time']:.2f} seconds")
                print(f"Settings used: {result['settings_used']}")
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