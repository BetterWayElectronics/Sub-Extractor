# BwE English Subtitle Extractor (ASS -> SRT)

BwE English Subtitle Extractor is a Python script that extracts English subtitles from video files, primarily those with the `.mkv` extension. It leverages `ffmpeg` to extract subtitles and logs every step of its operation for easy monitoring and troubleshooting. I made this because my Plex client for some reason cannot handle ASS/ASA subtitles and crashes near the end of every video. Having the SRT converted and extracted from the video means that transcoding doesn't need to happen and I can use Direct Play and load the SRT instead. This greatly improves CPU usage on my server and removes the crashing issue I had. Hopefully this app is useful for other people with similar issues or those who just want to extract subtitles. Feel free to change the language within the code if you don't want English subtitles. It does not support the extraction of SRT subs embedded within MKV, though this is possible with some code editing.

## Features

- **Extract & Convert English Subtitles:** Utilizes `ffmpeg` to extract English ASS/ASA subtitle streams from video files and converts them to SRT.
- **Directory Scanning:** Recursively searches through directories and subdirectories for `.mkv` files.
- **Logging:** Logs all operations, including errors and successful extractions, to an `extract_subs.log` file in the script's directory.
- **Cross-Platform:** Developed in Python 3.12.0, primarily designed for Windows applications but compatible with any system where Python and `ffmpeg` are installed.

## Requirements

- **Python:** Version 3.12.0 or later.
- **FFmpeg:** Must be installed and accessible via your system’s PATH.

## Usage

The script can be run from the command line. You can specify either a single video file or an entire directory containing video files.

Extract Subtitles from a Single Video File

    python BwE_Sub_Extractor.py "/path/to/video.mkv"

Extract Subtitles from All .mkv Files in a Directory

    python BwE_Sub_Extractor.py "/path/to/directory"

## How It Works

    Logging:
    Every run of the script is logged in extract_subs.log (located in the same directory as the script), including the time of execution and the arguments passed.

    Subtitle Extraction:
    The script builds and executes an ffmpeg command to extract English subtitles:

    ffmpeg -i <video_path> -map 0:s:m:language:eng -c:s srt <subtitle_path> -y

        Input File: The video file provided.
        Subtitle Mapping: Filters streams to select only the English subtitles (language:eng).
        Output: Saves the extracted subtitles as an SRT file in the same directory as the video.

    Error Handling:
        If the video file or directory is not found, an error is logged.
        If no English subtitles are present in the video, an error message along with the FFmpeg output is logged.

    Directory Processing:
    The script walks through a directory structure and processes each .mkv file it finds, applying the subtitle extraction process.

## Primary Use Case (Post-Compilation)

  This app is designed to be compiled as an exe using PyInstaller and set as an app to run when a torrent is completed. 
  
  For qBittorrent add it to 'Run external program' in the 'Downloads' tab like this:
  
    "D:\File\Location\BwE_Sub_Extractor.exe" "%F"

  Now all videos you download will automatically have an SRT made with the same filename so Plex can find it and use it easily.

## Secondary Use Case (Post-Compilation)

  If you have a series or an entire directory of shows you want to extract the SRT from then run the app against the path.

    BwE_Sub_Extractor.exe "D:\Neon Genesis Evangelion\"

  This will then grab all MKV videos and create subtitles for each of them. If you put it in a higher directory it will traverse everything below it.

## Code Overview

    log_message(message)
    Appends log messages with timestamps to extract_subs.log.

    extract_subtitles(video_path)
    Extracts English subtitles from a given video file using ffmpeg. It checks for the existence of the video file, executes the extraction command, and logs the results.

    process_directory(directory_path)
    Recursively scans the specified directory for .mkv files and extracts subtitles from each file.


This project is licensed under the MIT License. See the LICENSE file for details.
