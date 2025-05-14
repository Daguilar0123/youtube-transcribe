import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import os
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import zipfile

# import your existing CLI/GUI logic unchanged:
from youtube_transcribe import download_video, vtt_to_txt

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret")

# where the web-downloads will live on the server
DOWNLOAD_DIR = Path(__file__).parent / "downloads"
DOWNLOAD_DIR.mkdir(exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if not url:
            flash("Please enter a YouTube URL.")
            return redirect(url_for("index"))

        # clear out any old files
        for f in DOWNLOAD_DIR.iterdir():
            f.unlink()

        # call your download/transcribe functions
        download_video(url, DOWNLOAD_DIR)
        has_transcript = vtt_to_txt(DOWNLOAD_DIR)
        mp4_file = next(DOWNLOAD_DIR.glob("*.mp4"))
        if has_transcript:
            txt_file = next(DOWNLOAD_DIR.glob("*.txt"))
            zip_path = DOWNLOAD_DIR / "download_bundle.zip"
            with zipfile.ZipFile(zip_path, "w") as zf:
                zf.write(mp4_file, mp4_file.name)
                zf.write(txt_file, txt_file.name)
            return send_file(zip_path, as_attachment=True)
        else:
            # no transcript: send video file only
            return send_file(mp4_file, as_attachment=True)

    return render_template("index.html")