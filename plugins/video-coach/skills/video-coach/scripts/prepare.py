#!/usr/bin/env python3
"""video-coach 准备脚本（macOS / Windows / Linux 通用，仅用 Python 标准库）

定位最新练习视频 →（macOS）抢救 QuickTime 未存储录制 → 存档
→ 抽音频 → whisper 本地转写（有缓存则跳过）→ 每 20 秒抽一帧

需要 Python 3.8+。

用法:
  python3 prepare.py [视频文件]      不传参数时自动找最新的（Windows 用 python 或 py）
  python3 prepare.py --download-model  下载默认 whisper 模型（约 1.6GB）

可配置环境变量:
  VIDEO_COACH_DIR      视频存档目录（默认 macOS ~/Movies/录视频练习，Windows/Linux ~/Videos/录视频练习）
  VIDEO_COACH_MODEL    whisper 模型路径（默认 ~/.local/share/whisper/ggml-large-v3-turbo.bin）
  VIDEO_COACH_LANG     转写语言（默认 zh）
  VIDEO_COACH_WHISPER  whisper-cli 可执行文件路径（不在 PATH 里时用）
  HF_ENDPOINT          模型下载源（国内可设为 https://hf-mirror.com）
"""
import datetime
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

IS_MAC = sys.platform == "darwin"
IS_WIN = os.name == "nt"
HOME = Path.home()
VIDEO_EXTS = {".mov", ".mp4", ".m4v", ".mkv", ".webm"}
MODEL_NAME = "ggml-large-v3-turbo.bin"

VIDEO_DIR = Path(os.environ.get("VIDEO_COACH_DIR") or HOME / ("Movies" if IS_MAC else "Videos") / "录视频练习")
MODEL = Path(os.environ.get("VIDEO_COACH_MODEL") or HOME / ".local" / "share" / "whisper" / MODEL_NAME)
LANG_CODE = os.environ.get("VIDEO_COACH_LANG", "zh")
WORK = Path(tempfile.gettempdir()) / "video-coach"
QT_AUTOSAVE = HOME / "Library/Containers/com.apple.QuickTimePlayerX/Data/Library/Autosave Information"

if IS_MAC:
    INSTALL_FFMPEG = "brew install ffmpeg"
    INSTALL_WHISPER = "brew install whisper-cpp"
elif IS_WIN:
    INSTALL_FFMPEG = "winget install Gyan.FFmpeg（装完重开终端）"
    INSTALL_WHISPER = ("到 https://github.com/ggml-org/whisper.cpp/releases 下载 whisper-bin-x64.zip，"
                       "解压后把目录加入 PATH，或设置环境变量 VIDEO_COACH_WHISPER 指向 whisper-cli.exe")
else:
    INSTALL_FFMPEG = "sudo apt install ffmpeg（Fedora: sudo dnf install ffmpeg；Arch: sudo pacman -S ffmpeg）"
    INSTALL_WHISPER = ("git clone https://github.com/ggml-org/whisper.cpp && cd whisper.cpp && "
                       "cmake -B build && cmake --build build -j --config Release，"
                       "然后把 build/bin 加入 PATH 或设置 VIDEO_COACH_WHISPER")


def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def run(*cmd, **kw):
    return subprocess.run([str(c) for c in cmd], check=True, **kw)


def download_model():
    base = os.environ.get("HF_ENDPOINT", "https://huggingface.co").rstrip("/")
    url = f"{base}/ggerganov/whisper.cpp/resolve/main/{MODEL_NAME}"
    MODEL.parent.mkdir(parents=True, exist_ok=True)
    part = MODEL.with_suffix(".part")
    print(f"下载 {url}\n  → {MODEL}")

    def progress(blocks, block_size, total):
        if total > 0:
            print(f"\r  {min(blocks * block_size * 100 // total, 100)}%", end="", flush=True)

    urllib.request.urlretrieve(url, part, progress)
    part.replace(MODEL)
    print("\n完成")


def find_whisper():
    custom = os.environ.get("VIDEO_COACH_WHISPER")
    if custom:
        return custom if Path(custom).is_file() else die(f"VIDEO_COACH_WHISPER 指向的文件不存在：{custom}")
    # whisper.cpp 新版叫 whisper-cli，部分旧版 Linux 包叫 whisper-cpp
    return shutil.which("whisper-cli") or shutil.which("whisper-cpp") or die(f"缺少 whisper-cli：{INSTALL_WHISPER}")


def newest(paths):
    paths = [p for p in paths if p.is_file()]
    return max(paths, key=lambda p: p.stat().st_mtime) if paths else None


def rescue_quicktime(archived):
    """QuickTime 里录了但没按 ⌘S 的录制躺在 Autosave 里，比存档更新就抢救出来（仅 macOS）"""
    if not IS_MAC or not QT_AUTOSAVE.is_dir():
        return None
    autosave = newest(p for p in QT_AUTOSAVE.rglob("*.mov") if ".qtpxcomposition" in str(p.parent))
    if not autosave or (archived and autosave.stat().st_mtime <= archived.stat().st_mtime):
        return None
    n = len(list(VIDEO_DIR.glob("*-练习*.mov")))
    dest = VIDEO_DIR / f"{datetime.date.today():%Y-%m-%d}-练习{n + 1:02d}.mov"
    shutil.copy2(autosave, dest)
    print(f"已从 QuickTime 未存储录制抢救: {dest}")
    return dest


def main():
    # 输出给 agent 读取：统一 UTF-8，避免英文版 Windows 管道默认编码无法输出中文
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    if sys.argv[1:] == ["--download-model"]:
        return download_model()

    # 用完整路径调用：Windows 只会自动补 .exe，经 PATH 找到的 .cmd/.bat 包装脚本必须写全路径
    ffmpeg, ffprobe = (shutil.which(t) or die(f"缺少 {t}：{INSTALL_FFMPEG}") for t in ("ffmpeg", "ffprobe"))
    whisper = find_whisper()
    if not MODEL.is_file():
        die(f"缺少 whisper 模型：{MODEL}\n  运行 {Path(__file__).name} --download-model 自动下载"
            "（国内先设置环境变量 HF_ENDPOINT=https://hf-mirror.com）")

    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)

    if len(sys.argv) > 1:
        video = Path(sys.argv[1]).expanduser()
    else:
        archived = newest(p for p in VIDEO_DIR.iterdir() if p.suffix.lower() in VIDEO_EXTS)
        video = rescue_quicktime(archived) or archived
    if not video or not video.is_file():
        hint = "，QuickTime 里也没有未存储的录制" if IS_MAC else ""
        die(f"没找到视频：{VIDEO_DIR} 为空{hint}（也可以直接传视频路径）")
    video = video.resolve()

    duration = run(ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video,
                   capture_output=True, text=True).stdout.strip()

    transcript = video.with_name(f"{video.stem}-字幕.txt")
    if not transcript.is_file() or transcript.stat().st_size == 0:
        # 中间文件用 ASCII 名，避免 Windows 版 whisper-cli 处理中文路径出错
        wav = WORK / "audio.wav"
        run(ffmpeg, "-y", "-loglevel", "error", "-i", video, "-ar", "16000", "-ac", "1", wav)
        with open(transcript, "wb") as out:
            run(whisper, "-m", MODEL, "-l", LANG_CODE, "-f", wav, "-np", stdout=out, stderr=subprocess.DEVNULL)
        wav.unlink(missing_ok=True)

    frames_dir = WORK / f"frames-{re.sub(r'[^A-Za-z0-9_-]', '_', video.stem)}"
    shutil.rmtree(frames_dir, ignore_errors=True)
    frames_dir.mkdir(parents=True)
    run(ffmpeg, "-y", "-loglevel", "error", "-i", video, "-vf", "fps=1/20,scale=960:-1",
        frames_dir / "tmp_%03d.jpg")
    # 文件名带时间戳（f_0020s.jpg = 第 20 秒），交叉印证时直接对回字幕
    for i, f in enumerate(sorted(frames_dir.glob("tmp_*.jpg"))):
        f.rename(frames_dir / f"f_{i * 20:04d}s.jpg")

    print(f"VIDEO={video}")
    print(f"DURATION={int(float(duration or 0))}s")
    print(f"TRANSCRIPT={transcript}")
    print(f"FRAMES_DIR={frames_dir}")
    print(f"FRAMES={len(list(frames_dir.glob('f_*.jpg')))}")


if __name__ == "__main__":
    main()
