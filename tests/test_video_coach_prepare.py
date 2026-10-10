"""video-coach prepare.py 跨平台冒烟测试：用假的 ffmpeg / ffprobe / whisper-cli 跑完整流程。

本地运行：python3 -m unittest discover tests
CI 在 macOS / Windows / Ubuntu 上各跑一遍（.github/workflows/test.yml）。
"""
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREPARE = ROOT / "plugins/video-coach/skills/video-coach/scripts/prepare.py"
IS_WIN = os.name == "nt"

STUBS = {
    "ffprobe": "print('185.4')",
    "ffmpeg": (
        "import sys, pathlib\n"
        "out = sys.argv[-1]\n"
        "if 'tmp_%03d.jpg' in out:\n"
        "    for i in range(1, 11):\n"
        "        pathlib.Path(out.replace('%03d', f'{i:03d}')).write_bytes(b'x')\n"
        "else:\n"
        "    pathlib.Path(out).write_bytes(b'wav')\n"
    ),
    "whisper-cli": "import sys; sys.stdout.buffer.write('[00:00:00.000 --> 00:00:03.000]  大家好，今天聊聊表达。\\n'.encode('utf-8'))",
}


def make_stubs(bin_dir):
    for name, code in STUBS.items():
        script = bin_dir / f"{name}.py"
        script.write_text(code, encoding="utf-8")
        if IS_WIN:
            (bin_dir / f"{name}.cmd").write_text(f'@"{sys.executable}" "{script}" %*\r\n', encoding="ascii")
        else:
            launcher = bin_dir / name
            launcher.write_text(f'#!/bin/sh\nexec "{sys.executable}" "{script}" "$@"\n')
            launcher.chmod(0o755)


class PrepareTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.home, bin_dir = base / "home", base / "bin"
        self.home.mkdir()
        bin_dir.mkdir()
        make_stubs(bin_dir)
        self.env = dict(os.environ, HOME=str(self.home), USERPROFILE=str(self.home),
                        PATH=str(bin_dir) + os.pathsep + os.environ["PATH"],
                        TMPDIR=str(base), TEMP=str(base), TMP=str(base))
        for key in ("VIDEO_COACH_DIR", "VIDEO_COACH_MODEL", "VIDEO_COACH_WHISPER", "PYTHONIOENCODING", "PYTHONUTF8"):
            self.env.pop(key, None)
        self.video_dir = self.home / ("Movies" if sys.platform == "darwin" else "Videos") / "录视频练习"

    def tearDown(self):
        self.tmp.cleanup()

    def run_prepare(self, *args):
        # 故意不设 PYTHONIOENCODING：验证脚本自己把管道输出切到 UTF-8
        p = subprocess.run([sys.executable, str(PREPARE), *args], env=self.env, capture_output=True)
        return p.returncode, p.stdout.decode("utf-8"), p.stderr.decode("utf-8")

    def add_model(self):
        model = self.home / ".local/share/whisper/ggml-large-v3-turbo.bin"
        model.parent.mkdir(parents=True)
        model.write_bytes(b"m")

    def test_missing_model_gives_download_hint(self):
        code, _, err = self.run_prepare()
        self.assertEqual(code, 1)
        self.assertIn("--download-model", err)

    def test_empty_dir_reports_clearly(self):
        self.add_model()
        code, _, err = self.run_prepare()
        self.assertEqual(code, 1)
        self.assertIn("没找到视频", err)

    def test_full_run_on_newest_video(self):
        self.add_model()
        self.video_dir.mkdir(parents=True)
        old, new = self.video_dir / "2026-10-09-练习01.mov", self.video_dir / "2026-10-10-练习02.mov"
        old.write_bytes(b"v")
        new.write_bytes(b"v")
        os.utime(old, (time.time() - 100, time.time() - 100))

        code, out, err = self.run_prepare()
        self.assertEqual(code, 0, err)
        fields = dict(line.split("=", 1) for line in out.splitlines() if "=" in line)
        self.assertEqual(Path(fields["VIDEO"]).name, new.name)
        self.assertEqual(fields["DURATION"], "185s")
        self.assertEqual(fields["FRAMES"], "10")
        self.assertTrue((Path(fields["FRAMES_DIR"]) / "f_0180s.jpg").is_file())
        transcript = Path(fields["TRANSCRIPT"])
        self.assertEqual(transcript.name, "2026-10-10-练习02-字幕.txt")
        self.assertIn("大家好", transcript.read_text(encoding="utf-8"))

        # 第二次运行命中字幕缓存
        mtime = transcript.stat().st_mtime
        code, _, err = self.run_prepare(str(old))
        self.assertEqual(code, 0, err)
        self.assertEqual(transcript.stat().st_mtime, mtime)
        self.assertTrue((self.video_dir / "2026-10-09-练习01-字幕.txt").is_file())


if __name__ == "__main__":
    unittest.main()
