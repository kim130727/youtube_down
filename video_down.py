from pathlib import Path
import yt_dlp

URL = "https://www.youtube.com/live/ECY8cmMkLMs"

Path("downloads").mkdir(exist_ok=True)

def hook(d):
    status = d.get("status")
    if status == "downloading":
        downloaded = d.get("downloaded_bytes", 0)
        total = d.get("total_bytes") or d.get("total_bytes_estimate")
        if total:
            percent = downloaded / total * 100
            print(f"다운로드 중: {percent:.1f}%")
        else:
            print("다운로드 중...")
    elif status == "finished":
        print("다운로드 완료, 후처리 중...")

ydl_opts = {
    "outtmpl": "downloads/%(title)s.%(ext)s",
    "live_from_start": True,
    "format": "bestvideo+bestaudio/best",
    "merge_output_format": "mp4",
    "retries": 10,
    "fragment_retries": 10,
    "concurrent_fragment_downloads": 3,
    "progress_hooks": [hook],
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([URL])
except Exception as e:
    print(f"다운로드 실패: {e}")