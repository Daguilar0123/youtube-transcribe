import sys, os, subprocess
from pathlib import Path
from yt_dlp import YoutubeDL
import tkinter as tk
from tkinter import messagebox

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


# Process function for both CLI and GUI
def process(url: str, raw_name: str):
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

def main():
    if len(sys.argv) < 2:
        print("Usage: python youtube_transcribe.py <URL> [FolderName]")
        sys.exit(1)
    url = sys.argv[1]
    raw_name = sys.argv[2] if len(sys.argv) > 2 else "YouTube Downloads"
    process(url, raw_name)


# GUI entrypoint
def gui_main():
    root = tk.Tk()
    root.title("YouTube Transcribe")

    tk.Label(root, text="YouTube URL:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    url_entry = tk.Entry(root, width=50)
    url_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="Project Folder Name:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    folder_entry = tk.Entry(root, width=50)
    folder_entry.grid(row=1, column=1, padx=5, pady=5)

    def on_download():
        url = url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return
        raw_name = folder_entry.get().strip() or "YouTube Downloads"
        root.destroy()
        process(url, raw_name)

    download_btn = tk.Button(root, text="Download & Transcribe", command=on_download)
    download_btn.grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()


if __name__ == "__main__":
    # Uncomment one of the following:
    # main()      # for command-line use
    gui_main()    # for GUI use