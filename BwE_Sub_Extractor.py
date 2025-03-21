import os
import sys
import subprocess
from datetime import datetime

# Define log file in the same directory as the script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "extract_subs.log")

def log_message(message):
    # Append log messages to extract_subs.log in the script's directory.
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

# Log script execution
log_message(f"Script started with arguments: {sys.argv}")

def extract_subtitles(video_path):
    # Extract English subtitles from a single video file.
    if not os.path.isfile(video_path):
        log_message(f"ERROR: File not found - {video_path}")
        return

    # Get video file directory and name
    file_dir, file_name = os.path.split(video_path)
    file_base, _ = os.path.splitext(file_name)

    # Set subtitle file path (same folder as video)
    subtitle_path = os.path.join(file_dir, f"{file_base}.eng.srt")

    # FFmpeg command to extract English subtitles
    ffmpeg_cmd = [
        "ffmpeg", "-i", video_path, 
        "-map", "0:s:m:language:eng", "-c:s", "srt", subtitle_path, "-y"
    ]

    try:
        print(f"Extracting English subtitles from: {video_path}")
        result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if os.path.exists(subtitle_path):
            success_message = f"SUCCESS: Subtitles saved to {subtitle_path}"
            print(success_message)
            log_message(success_message)
        else:
            error_message = f"ERROR: No English subtitles found in {video_path}\nFFmpeg Output:\n{result.stderr}"
            print(error_message)
            log_message(error_message)

    except subprocess.CalledProcessError as e:
        error_message = f"ERROR: FFmpeg failed to process {video_path}\nError: {str(e)}"
        print(error_message)
        log_message(error_message)

def process_directory(directory_path):
    # Find all .mkv files in a directory and subdirectories and extract subtitles from them.
    if not os.path.isdir(directory_path):
        log_message(f"ERROR: Directory not found - {directory_path}")
        return

    log_message(f"Scanning directory: {directory_path}")
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(".mkv"):
                video_file = os.path.join(root, file)
                extract_subtitles(video_file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        script_name = os.path.basename(sys.argv[0])
        print("BwE English Subtitle Extractor (SRT)\n")

        if script_name.endswith(".py"):
            print(f"Usage: python {script_name} <video_file_or_directory>")
        else:
            print(f"Usage: {script_name} <video_file_or_directory>")
            
        sys.exit(1)

    input_path = sys.argv[1]

    if os.path.isdir(input_path):
        process_directory(input_path)
    else:
        extract_subtitles(input_path)
