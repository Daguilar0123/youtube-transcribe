import sys, os, subprocess
from pathlib import Path
from yt_dlp import YoutubeDL

def sanitize(name: str) -> str:
    # allow letters, numbers, spaces, dots, underscores, hyphens
    return "".join(c if c.isalnum() or c in " ._-"
                   else "_" for c in name).strip()

def download_video(url: str, folder: Path) -> None:
    opts = {
        "format": "bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/mp4",
        "merge_output_format": "mp4",
        "outtmpl": str(folder / "%(title)s.%(ext)s"),
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
    }
    with YoutubeDL(opts) as ydl:
        ydl.download([url])

def vtt_to_txt(folder: Path) -> bool:
    any_subs = False
    for vtt in folder.glob("*.en.vtt"):
        any_subs = True
        txt = vtt.with_suffix(".txt")
        lines = []
        for line in vtt.read_text(encoding="utf-8").splitlines():
            if line.strip() == "" or "-->" in line or line.strip().isdigit():
                continue
            lines.append(line)
        txt.write_text("\n".join(lines), encoding="utf-8")
    return any_subs

def notify(title: str, message: str):
    subprocess.run([
        "osascript", "-e",
        f'display notification "{message}" with title "{title}"'
    ])

def main():
    if len(sys.argv) < 2:
        print("Usage: python youtube_transcribe.py <URL> [FolderName]")
        sys.exit(1)
    url = sys.argv[1]
    raw_name = sys.argv[2] if len(sys.argv) > 2 else "YouTube Downloads"
    safe = sanitize(raw_name)
    project = Path.home() / "Downloads" / safe
    project.mkdir(parents=True, exist_ok=True)

    print(f"Downloading into: {project}")
    download_video(url, project)
    if vtt_to_txt(project):
        notify("YouTube Automation",
               f"Download & transcript saved in {project}")
    else:
        notify("YouTube Automation",
               f"Download complete but no subtitles in {project}")
        
if __name__ == "__main__":
    main()