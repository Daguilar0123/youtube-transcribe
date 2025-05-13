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

## Usage

```bash
git clone https://github.com/Daguilar0123/youtube-transcribe.git
cd youtube-transcribe
pip install yt-dlp
python3 youtube_transcribe.py "<YouTube URL>" "My Project Name"
```

## 📦 macOS “YouTube Transcribe” App

We’ve packaged a one-click Automator app with a custom icon:

1. **Clone or download** this repo.
2. **Open** the `macos/` folder.
3. **Drag** `YouTube Transcribe.app` into your `/Applications` folder.
4. **(Optional)** Right-click its icon in the Dock → **Options → Keep in Dock**.
5. On first launch, you may need to allow it in **System Preferences → Security & Privacy**.

That’s it—now anyone can run the same app (with icon) you’re using!  