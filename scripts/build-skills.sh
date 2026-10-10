#!/usr/bin/env bash
# 把 plugins/*/skills/<name>/ 打包成 dist/<name>.skill（zip），供 Claude 桌面版 / 网页版安装
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf dist && mkdir -p dist
for dir in plugins/*/skills/*/; do
  name=$(basename "$dir")
  (cd "$(dirname "$dir")" && zip -qr -X "$OLDPWD/dist/$name.skill" "$name" -x '*.DS_Store')
  echo "dist/$name.skill"
done
