#!/usr/bin/env bash
# drama-commerce skill installer (macOS / Linux / Git Bash)
# 用法：
#   ./install.sh                     自动探测 WorkBuddy / Claude Code 目录
#   ./install.sh ~/.claude/skills    指定 skills 目录
set -e

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="drama-commerce"

if [ -n "${1:-}" ]; then
  TARGET="$1"
elif [ -d "$HOME/.workbuddy" ]; then
  TARGET="$HOME/.workbuddy/skills"
elif [ -d "$HOME/.claude" ]; then
  TARGET="$HOME/.claude/skills"
else
  TARGET="$HOME/.claude/skills"
fi

DEST="$TARGET/$SKILL_NAME"

if [ -d "$DEST" ]; then
  BACKUP="$DEST.bak.$(date +%Y%m%d%H%M%S)"
  echo "已存在，备份到：$BACKUP"
  mv "$DEST" "$BACKUP"
fi

mkdir -p "$TARGET"
# 整目录复制，随后剔除仓库元数据（.git 等不应进入安装目录）
cp -R "$SRC_DIR/." "$DEST/"

for x in .git .github examples scripts install.sh install.ps1 \
         CONTRIBUTING.md CHANGELOG.md; do
  rm -rf "$DEST/$x"
done

echo ""
echo "✅ 安装完成：$DEST"
echo "   文件清单："
find "$DEST" -type f | sed "s|$DEST/|     |" | sort
echo ""
echo "👉 重启会话后说「帮我做一条短剧带货视频」即可触发。"
