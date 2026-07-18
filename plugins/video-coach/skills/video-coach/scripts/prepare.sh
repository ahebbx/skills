#!/bin/bash
# video-coach 准备脚本:定位最新练习视频 → 抢救 QuickTime 未存储录制 → 存档
# → 抽音频 → whisper 本地转写(有缓存则跳过) → 每 20 秒抽一帧
# 用法: prepare.sh [视频文件]   不传参数时自动找最新的
# 可配置环境变量:
#   VIDEO_COACH_DIR    视频存档目录(默认 ~/Movies/录视频练习)
#   VIDEO_COACH_MODEL  whisper 模型路径(默认 ~/.local/share/whisper/ggml-large-v3-turbo.bin)
#   VIDEO_COACH_LANG   转写语言(默认 zh)
set -euo pipefail

VIDEO_DIR="${VIDEO_COACH_DIR:-$HOME/Movies/录视频练习}"
MODEL="${VIDEO_COACH_MODEL:-$HOME/.local/share/whisper/ggml-large-v3-turbo.bin}"
LANG_CODE="${VIDEO_COACH_LANG:-zh}"
WORK="${TMPDIR:-/tmp}/video-coach"
QT_AUTOSAVE="$HOME/Library/Containers/com.apple.QuickTimePlayerX/Data/Library/Autosave Information"

die() { echo "ERROR: $*" >&2; exit 1; }
command -v ffmpeg >/dev/null || die "缺少 ffmpeg:brew install ffmpeg"
command -v whisper-cli >/dev/null || die "缺少 whisper-cli:brew install whisper-cpp"
[ -f "$MODEL" ] || die "缺少 whisper 模型:curl -L -o '$MODEL' https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin(国内可换 hf-mirror.com)"

mkdir -p "$VIDEO_DIR" "$WORK"

newest_in_dir() {
  find "$VIDEO_DIR" -maxdepth 1 -type f \( -iname "*.mov" -o -iname "*.mp4" -o -iname "*.m4v" \) -print0 2>/dev/null \
    | xargs -0 ls -t 2>/dev/null | head -1
}

VIDEO="${1:-}"
if [ -z "$VIDEO" ]; then
  ARCHIVED=$(newest_in_dir || true)
  # QuickTime 里录了但没按 ⌘S 的录制,躺在 Autosave 里,比存档更新就抢救出来
  AUTOSAVE=$(find "$QT_AUTOSAVE" -name "*.mov" -path "*.qtpxcomposition/*" -print0 2>/dev/null \
    | xargs -0 ls -t 2>/dev/null | head -1 || true)
  if [ -n "$AUTOSAVE" ] && { [ -z "$ARCHIVED" ] || [ "$AUTOSAVE" -nt "$ARCHIVED" ]; }; then
    N=$(find "$VIDEO_DIR" -maxdepth 1 -name "*-练习*.mov" 2>/dev/null | wc -l | tr -d ' ')
    DEST="$VIDEO_DIR/$(date +%F)-练习$(printf '%02d' $((N + 1))).mov"
    cp "$AUTOSAVE" "$DEST"
    echo "已从 QuickTime 未存储录制抢救: $DEST"
    VIDEO="$DEST"
  else
    VIDEO="$ARCHIVED"
  fi
fi
[ -n "$VIDEO" ] && [ -f "$VIDEO" ] || die "没找到视频:$VIDEO_DIR 为空,QuickTime 里也没有未存储的录制"

BASE="${VIDEO%.*}"
DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO")

TRANSCRIPT="$BASE-字幕.txt"
if [ ! -s "$TRANSCRIPT" ]; then
  WAV="$WORK/$(basename "$BASE").wav"
  ffmpeg -y -loglevel error -i "$VIDEO" -ar 16000 -ac 1 "$WAV"
  whisper-cli -m "$MODEL" -l "$LANG_CODE" -f "$WAV" -np 2>/dev/null > "$TRANSCRIPT"
  rm -f "$WAV"
fi

FRAMES_DIR="$WORK/frames-$(basename "$BASE")"
rm -rf "$FRAMES_DIR" && mkdir -p "$FRAMES_DIR"
ffmpeg -y -loglevel error -i "$VIDEO" -vf "fps=1/20,scale=960:-1" "$FRAMES_DIR/tmp_%03d.jpg"
# 文件名带时间戳(f_0020s.jpg = 第 20 秒),交叉印证时直接对回字幕
i=0
for f in "$FRAMES_DIR"/tmp_*.jpg; do
  mv "$f" "$FRAMES_DIR/f_$(printf '%04d' $((i * 20)))s.jpg"
  i=$((i + 1))
done

echo "VIDEO=$VIDEO"
echo "DURATION=${DURATION%.*}s"
echo "TRANSCRIPT=$TRANSCRIPT"
echo "FRAMES_DIR=$FRAMES_DIR"
echo "FRAMES=$(ls "$FRAMES_DIR" | wc -l | tr -d ' ')"
