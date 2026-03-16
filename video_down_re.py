#라이브 처음부터 다운로드
#영상 + 음성 자동 병합
#네트워크 끊김 자동 재시도

import yt_dlp

URL = "https://www.youtube.com/live/ECY8cmMkLMs"

ydl_opts = {
    "outtmpl": "downloads/%(title)s.%(ext)s",
    "live_from_start": True,

    "format": "bestvideo+bestaudio/best",
    "merge_output_format": "mp4",

    "retries": 10,
    "fragment_retries": 10,

    "concurrent_fragment_downloads": 3,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([URL])