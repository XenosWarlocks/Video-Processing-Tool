# proj/src/video_processing/video_compressor.py

import os
import logging
import ffmpeg

class VideoCompressor:
    # Bitrate constraints
    MIN_TOTAL_BITRATE = 11000  # bps
    MIN_AUDIO_BITRATE = 32000  # bps
    MAX_AUDIO_BITRATE = 256000  # bps
    MIN_VIDEO_BITRATE = 100000  # bps

    @classmethod
    def compress_video(
        cls,
        video_path: str, 
        target_size_kb: int = 1024,  # Default 1MB
        two_pass: bool = True,
        filename_suffix: str = 'compressed_'
    ) -> str:
        """
        Intelligently compress video to target size with advanced bitrate management.
        
        Args:
            video_path (str): Full path to the input video
            target_size_kb (int): Target file size in kilobytes
            two_pass (bool): Enable two-pass encoding for better quality
            filename_suffix (str): Suffix for output filename
        
        Returns:
            str: Path to compressed video or False if compression fails
        """
        try:
            # Validate input file
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Input video file not found: {video_path}")

            # Generate output filename
            filename, ext = os.path.splitext(video_path)
            output_path = f"{filename}_{filename_suffix}.mp4"

            # Probe video metadata
            probe = ffmpeg.probe(video_path)
            video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
            
            # Calculate video duration
            duration = float(probe['format']['duration'])
            
            # Get audio bitrate (if exists)
            audio_stream = next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)
            audio_bitrate = float(audio_stream['bit_rate']) if audio_stream else cls.MIN_AUDIO_BITRATE

            # Calculate target total bitrate
            target_total_bitrate = (target_size_kb * 1024 * 8) / (1.073741824 * duration)

            # Validate bitrate
            if target_total_bitrate < cls.MIN_TOTAL_BITRATE:
                logging.warning(f"Target bitrate {target_total_bitrate} is extremely low. Compression may fail.")
                return False

            # Adjust audio bitrate
            if 10 * audio_bitrate > target_total_bitrate:
                audio_bitrate = max(
                    min(target_total_bitrate / 10, cls.MAX_AUDIO_BITRATE), 
                    cls.MIN_AUDIO_BITRATE
                )

            # Calculate video bitrate
            video_bitrate = target_total_bitrate - audio_bitrate
            if video_bitrate < 1000:
                logging.error(f"Video bitrate {video_bitrate} is too low for compression.")
                return False

            # Compression with two-pass option
            input_stream = ffmpeg.input(video_path)
            
            if two_pass:
                # First pass
                (
                    input_stream
                    .output(os.devnull, 
                        **{
                            'c:v': 'libx264', 
                            'b:v': f'{int(video_bitrate)}', 
                            'pass': 1, 
                            'f': 'mp4'
                        }
                    )
                    .overwrite_output()
                    .run(capture_stdout=True, capture_stderr=True)
                )

                # Second pass
                (
                    input_stream
                    .output(
                        output_path, 
                        **{
                            'c:v': 'libx264', 
                            'b:v': f'{int(video_bitrate)}', 
                            'pass': 2, 
                            'c:a': 'aac', 
                            'b:a': f'{int(audio_bitrate)}'
                        }
                    )
                    .overwrite_output()
                    .run(capture_stdout=True, capture_stderr=True)
                )
            else:
                # Single pass compression
                (
                    input_stream
                    .output(
                        output_path, 
                        **{
                            'c:v': 'libx264', 
                            'b:v': f'{int(video_bitrate)}', 
                            'c:a': 'aac', 
                            'b:a': f'{int(audio_bitrate)}'
                        }
                    )
                    .overwrite_output()
                    .run(capture_stdout=True, capture_stderr=True)
                )

            # Verify output size
            output_size = os.path.getsize(output_path) / 1024  # KB
            logging.info(f"Compressed video size: {output_size:.2f} KB (Target: {target_size_kb} KB)")

            # Recursive compression if size is still too large
            if output_size > target_size_kb:
                logging.warning("Initial compression didn't meet size requirements. Attempting recursive compression.")
                return cls.compress_video(
                    output_path, 
                    target_size_kb, 
                    two_pass, 
                    filename_suffix + 'retry_'
                )

            return output_path

        except ffmpeg.Error as e:
            logging.error(f"FFmpeg error: {e.stderr.decode()}")
            return False
        except Exception as e:
            logging.error(f"Unexpected compression error: {e}")
            return False

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Example usage
if __name__ == "__main__":
    video_path = r"C:\Users\mannu\Downloads\JSproj\megaProj\vid_pro_tool\src\video_processing\sample\Transformers.mkv"
    compressed_video = VideoCompressor.compress_video(
        video_path, 
        target_size_kb=1024,  # 1MB target
        two_pass=True
    )
    
    if compressed_video:
        print(f"Video compressed successfully: {compressed_video}")
    else:
        print("Video compression failed.")


# python src/video_processing/video_compressor.py
