import subprocess

def cut_video_more_accurate(input_file, start, end, output_file):
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
    subprocess.run(cmd, check=True)

cut_video_more_accurate(
    "downloads/video.mp4",
    "00:43:11",
    "01:26:55",
    "downloads/video_cut.mp4"
)