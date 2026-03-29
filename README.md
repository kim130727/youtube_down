# YouTube 다운로드 + 컷팅 프로젝트

이 프로젝트는 아래 2개 파이썬 파일로 구성됩니다.

1. `download_youtube.py`: YouTube URL을 `downloads/video.mp4`로 다운로드
2. `cut_video.py`: `downloads/video.mp4`를 원하는 구간으로 잘라 `cut/` 폴더에 저장 (진행률 바 표시)

## 폴더 구조

```text
youtube_down/
├─ download_youtube.py
├─ cut_video.py
├─ downloads/
│  └─ video.mp4
└─ cut/
   └─ video_cut.mp4
```

## 사전 준비

1. Python 3.11+
2. `yt-dlp` 설치
3. `ffmpeg` 설치 후 시스템 PATH 등록

예시(`uv` 사용 시):

```bash
uv sync
```

## 1) 유튜브 다운로드

```bash
python download_youtube.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

기본 출력:
- `downloads/video.mp4`

출력 파일 경로를 바꾸고 싶으면:

```bash
python download_youtube.py "URL" --output downloads/my_video.mp4
```

## 2) 영상 컷팅 (진행률 바 포함)

```bash
python cut_video.py --start 00:35:46 --end 01:23:57
```

기본 입력/출력:
- 입력: `downloads/video.mp4`
- 출력: `cut/video_cut.mp4`

직접 지정도 가능합니다:

```bash
python cut_video.py --input downloads/video.mp4 --start 00:10:00 --end 00:12:30.500 --output cut/highlight.mp4
```

## 시간 정확도 관련

- 컷팅은 FFmpeg에서 `-ss/-to`를 입력 뒤(`-i` 뒤)로 두고 재인코딩(`libx264`, `aac`)하여, 빠른 컷팅보다 시간 오차를 줄이는 방식으로 처리합니다.

## 참고

- `downloads/video.mp4`가 없으면 `cut_video.py`는 에러를 출력합니다.
- `ffmpeg`가 PATH에 없으면 컷팅이 실패합니다.
