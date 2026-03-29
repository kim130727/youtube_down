from __future__ import annotations

import argparse
from pathlib import Path

from yt_dlp import YoutubeDL


DEFAULT_OUTPUT = Path("downloads") / "video.mp4"


def download_youtube_video(url: str, output_path: Path = DEFAULT_OUTPUT) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        "outtmpl": str(output_path.with_suffix(".%(ext)s")),
        "format": "bestvideo*+bestaudio/best",
        "merge_output_format": "mp4",
        "recodevideo": "mp4",
        "noplaylist": True,
        "retries": 20,
        "fragment_retries": 20,
        "concurrent_fragment_downloads": 1,
        "quiet": False,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    if not output_path.exists():
        raise FileNotFoundError(f"다운로드가 완료되었지만 파일을 찾지 못했습니다: {output_path}")

    return output_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="YouTube URL을 downloads/video.mp4로 다운로드합니다."
    )
    parser.add_argument("url", help="다운로드할 YouTube URL")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help=f"출력 파일 경로 (기본값: {DEFAULT_OUTPUT})",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    output_path = Path(args.output)
    saved = download_youtube_video(args.url, output_path)
    print(f"완료: {saved}")


if __name__ == "__main__":
    main()
