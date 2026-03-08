import yt_dlp

URL = "https://www.youtube.com/live/ZxFaLv-8doc?si=qTnQ7KONjwib9sOH"

ydl_opts = {
    "outtmpl": "downloads/%(title)s.%(ext)s",
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([URL])