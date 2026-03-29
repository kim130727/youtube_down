from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


DEFAULT_INPUT = Path("downloads") / "video.mp4"
DEFAULT_OUTPUT_DIR = Path("cut")


def hms_to_seconds(hms: str) -> float:
    parts = hms.split(":")
    if len(parts) != 3:
        raise ValueError("시간 형식은 HH:MM:SS 또는 HH:MM:SS.mmm 이어야 합니다.")

    h, m, s = parts
    return int(h) * 3600 + int(m) * 60 + float(s)


def progress_bar(percent: int, width: int = 30) -> str:
    filled = int(width * percent / 100)
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def cut_video_with_progress(input_file: Path, start: str, end: str, output_file: Path) -> None:
    total_duration = hms_to_seconds(end) - hms_to_seconds(start)
    if total_duration <= 0:
        raise ValueError("end는 start보다 커야 합니다.")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    # 정확한 컷팅을 위해 -ss/-to를 입력(-i) 뒤에 배치하고 재인코딩합니다.
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_file),
        "-ss",
        start,
        "-to",
        end,
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        str(output_file),
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )

    time_pattern = re.compile(r"time=(\d+):(\d+):(\d+(?:\.\d+)?)")
    last_percent = -1

    if process.stdout is None:
        raise RuntimeError("FFmpeg 출력 스트림을 읽을 수 없습니다.")

    for line in process.stdout:
        match = time_pattern.search(line)
        if not match:
            continue

        hh = int(match.group(1))
        mm = int(match.group(2))
        ss = float(match.group(3))
        current = hh * 3600 + mm * 60 + ss

        percent = min(100, int(current / total_duration * 100))
        if percent == last_percent:
            continue

        bar = progress_bar(percent)
        print(f"\r{bar} {percent}%  ({current:.1f}/{total_duration:.1f}초)", end="")
        last_percent = percent

    process.wait()
    print()

    if process.returncode != 0:
        raise RuntimeError(f"FFmpeg 실패: exit={process.returncode}")

    print(f"완료: {output_file}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="다운로드된 비디오를 정확한 시간 기준으로 컷팅하고 진행률 바를 표시합니다."
    )
    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT),
        help=f"입력 비디오 경로 (기본값: {DEFAULT_INPUT})",
    )
    parser.add_argument("--start", required=True, help="시작 시간 (HH:MM:SS 또는 HH:MM:SS.mmm)")
    parser.add_argument("--end", required=True, help="종료 시간 (HH:MM:SS 또는 HH:MM:SS.mmm)")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_DIR / "video_cut.mp4"),
        help=f"출력 비디오 경로 (기본값: {DEFAULT_OUTPUT_DIR / 'video_cut.mp4'})",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    input_file = Path(args.input)
    output_file = Path(args.output)

    if not input_file.exists():
        raise FileNotFoundError(f"입력 파일을 찾을 수 없습니다: {input_file}")

    cut_video_with_progress(input_file, args.start, args.end, output_file)


if __name__ == "__main__":
    main()
