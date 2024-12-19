import os
import logging
import pathlib
import subprocess
from typing import Optional, Dict, Any

class VideoCompressor:
    @staticmethod
    def find_ffmpeg() -> Optional[str]:
        """Find FFmpeg executable path on Windows"""
        ffmpeg_path = r"C:\Users\{YOU}\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1-full_build\bin\ffmpeg.exe"
        # Change {YOU} to your path name
        
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
            print(f"FFprobe error: {e.stderr}")
            raise

    @staticmethod
    def list_sample_folder_contents():
        """List contents of the sample folder with detailed path information"""
        try:
            script_path = pathlib.Path(__file__).resolve()
            print(f"\nScript location: {script_path}")
            
            project_root = script_path.parents[2]
            print(f"Project root: {project_root}")
            
            sample_folder = project_root / 'src' / 'video_processing' / 'sample'
            print(f"Sample folder path: {sample_folder}")
            
            sample_folder.mkdir(parents=True, exist_ok=True)
            
            print("\nDirectory contents:")
            for item in sample_folder.iterdir():
                size = item.stat().st_size / 1024  # KB
                print(f"- {item.name} (Size: {size:.2f} KB)")
                print(f"  Absolute path: {item.absolute()}")
                print(f"  Exists: {item.exists()}")
                print(f"  Is file: {item.is_file()}")
                print(f"  Read permission: {os.access(str(item), os.R_OK)}")
                
        except Exception as e:
            print(f"Error during path checking: {e}")
            raise
    
    @classmethod
    def compress_video(
        cls,
        input_path: str, 
        target_size_kb: int = 1024,
        two_pass: bool = True,
        filename_suffix: str = 'compressed'
    ) -> str:
        """Compress video using FFmpeg subprocess"""
        try:
            # Find FFmpeg
            ffmpeg_path = cls.find_ffmpeg()
            if not ffmpeg_path:
                raise FileNotFoundError("FFmpeg executable not found")
            print(f"Found FFmpeg at: {ffmpeg_path}")
            
            # Convert input path to Path object
            video_path = pathlib.Path(input_path).resolve()
            print(f"\nProcessing video:")
            print(f"Input path: {video_path}")
            print(f"Exists: {video_path.exists()}")
            print(f"Is file: {video_path.is_file()}")
            print(f"Read permission: {os.access(str(video_path), os.R_OK)}")

            if not video_path.exists():
                raise FileNotFoundError(f"Video file not found: {video_path}")
            
            if not video_path.is_file():
                raise ValueError(f"Path is not a file: {video_path}")
            
            if not os.access(str(video_path), os.R_OK):
                raise PermissionError(f"No read permission for file: {video_path}")

            # Create output path
            output_path = video_path.parent / f"{video_path.stem}_{filename_suffix}{video_path.suffix}"
            print(f"Output path will be: {output_path}")

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Get video info
            try:
                probe_data = cls.probe_video(ffmpeg_path, str(video_path))
                stream_data = probe_data.get('streams', [{}])[0]
                format_data = probe_data.get('format', {})
                
                duration = float(format_data.get('duration', 0))
                width = stream_data.get('width', '?')
                height = stream_data.get('height', '?')
                codec = stream_data.get('codec_name', 'unknown')
                
                print(f"\nVideo Information:")
                print(f"Duration: {duration:.2f} seconds")
                print(f"Codec: {codec}")
                print(f"Resolution: {width}x{height}")
                
                # Calculate target bitrate (bits per second)
                target_size_bits = target_size_kb * 8 * 1024  # Convert KB to bits
                bitrate = int(target_size_bits / duration)
                
                # Prepare FFmpeg command
                cmd = [
                    ffmpeg_path,
                    '-y',  # Overwrite output file if it exists
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
                
                print("\nStarting compression...")
                print(f"Target bitrate: {bitrate/1024/1024:.2f} Mbps")
                
                # Run FFmpeg
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode != 0:
                    print(f"FFmpeg error: {result.stderr}")
                    raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)
                
                if output_path.exists():
                    final_size = output_path.stat().st_size / 1024  # KB
                    print(f"\nCompression complete!")
                    print(f"Final size: {final_size:.2f} KB")
                    return str(output_path)
                else:
                    raise RuntimeError("Output file was not created")
                
            except subprocess.CalledProcessError as e:
                print(f"FFmpeg process error: {e.stderr}")
                raise
            except Exception as e:
                print(f"Error during video processing: {e}")
                raise

        except Exception as e:
            print(f"Error: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            return False

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# python src/video_processing/video_compressor.py
