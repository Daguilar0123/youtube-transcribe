# YouTube Transcribe

A simple Python script to download a YouTube video (H.264/AAC plus YouTube’s auto-captions)
into `~/Downloads/<ProjectName>/`, then convert any `.en.vtt` subtitles into a human-readable
`.txt` transcript.

## Features

- Downloads best MP4 (H.264/AAC) via `yt-dlp`  
- Fetches English auto-subtitles (`.en.vtt`) if available  
- Strips out timestamps to produce a clean `.txt` transcript  
- Sends a macOS notification when complete

## Requirements

### Installing Python

If you don't have Python installed already, follow one of these easy methods:

- **Homebrew (macOS)**  
  Open Terminal and run:
  ```bash
  brew install python3
  ```
- **Official Installer**  
  Download and run the installer for your system from:
  https://www.python.org/downloads/

- Python 3.8+  
- macOS (for `osascript` notifications)  
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)  

```bash
pip install yt-dlp