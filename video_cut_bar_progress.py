import subprocess
import re

def hms_to_seconds(hms: str) -> float:
    h, m, s = hms.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)

def progress_bar(percent: int, width: int = 30) -> str:
    filled = int(width * percent / 100)
    return "[" + "#" * filled + "-" * (width - filled) + "]"

def cut_video_with_progress(input_file, start, end, output_file):
    total_duration = hms_to_seconds(end) - hms_to_seconds(start)
    if total_duration <= 0:
        raise ValueError("end는 start보다 커야 합니다.")

    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-ss", str(start),
        "-to", str(end),
        "-c:v", "libx264",
        "-c:a", "aac",
        output_file,
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1
    )

    time_pattern = re.compile(r"time=(\d+):(\d+):(\d+(?:\.\d+)?)")
    last_percent = -1

    for line in process.stdout:
        match = time_pattern.search(line)
        if match:
            hh = int(match.group(1))
            mm = int(match.group(2))
            ss = float(match.group(3))
            current = hh * 3600 + mm * 60 + ss

            percent = min(100, int(current / total_duration * 100))
            if percent != last_percent:
                bar = progress_bar(percent)
                print(f"\r{bar} {percent}%  ({current:.1f}/{total_duration:.1f}초)", end="")
                last_percent = percent

    process.wait()
    print()

    if process.returncode != 0:
        raise RuntimeError(f"FFmpeg 실패: exit={process.returncode}")

    print("완료:", output_file)