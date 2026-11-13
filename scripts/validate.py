#!/usr/bin/env python3
"""drama-commerce 仓库自检

检查项：
  1. SKILL.md frontmatter 是否存在且合法（name 小写连字符、description 长度 20-1024）
  2. SKILL.md 内引用的相对路径文件是否都存在
  3. references/ 下每个文件是否都被 SKILL.md 引用（避免孤儿文件）
  4. 全仓库 Markdown 内是否有未替换的占位符（TODO / <your-org> 等）

用法：
  python scripts/validate.py           # 在仓库根目录执行
  python scripts/validate.py --root .  # 指定根目录

退出码 0 = 全部通过，1 = 存在问题。
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
PLACEHOLDER_RE = re.compile(r"\bTODO\b|<your-org>|FIXME|XXX")

REQUIRED_REFERENCE_SECTIONS = ("references",)


def parse_frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        return {}
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if re.match(r"^\s", line):  # 嵌套字段（如 metadata.version）跳过
            continue
        k, sep, v = line.partition(":")
        if sep:
            fm[k.strip()] = v.strip()
    return fm


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root = pathlib.Path(args.root).resolve()

    errors: list[str] = []
    warns: list[str] = []

    skill = root / "SKILL.md"
    if not skill.exists():
        print("✗ 找不到 SKILL.md")
        return 1

    text = skill.read_text(encoding="utf-8")

    # 1. frontmatter
    fm = parse_frontmatter(text)
    if not fm:
        errors.append("SKILL.md 缺少 frontmatter（--- 包裹的 YAML 头）")
    else:
        name = fm.get("name", "")
        desc = fm.get("description", "")
        if not NAME_RE.match(name):
            errors.append(f"name 不合规：{name!r}（要求小写字母/数字/连字符，1-64 位）")
        if name and root.name != name:
            warns.append(f"name={name!r} 与目录名 {root.name!r} 不一致（部分平台要求一致）")
        if not (20 <= len(desc) <= 1024):
            errors.append(f"description 长度 {len(desc)}，要求 20-1024")
        if "license" not in fm:
            warns.append("frontmatter 建议补 license 字段")

    # 2. 相对链接
    for target in LINK_RE.findall(text):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        clean = target.split("#", 1)[0]
        if not clean:
            continue
        if not (root / clean).exists():
            errors.append(f"SKILL.md 引用的文件不存在：{clean}")

    # 3. 孤儿参考文件
    for section in REQUIRED_REFERENCE_SECTIONS:
        d = root / section
        if not d.is_dir():
            continue
        for f in sorted(d.glob("*.md")):
            rel = f"{section}/{f.name}"
            if rel not in text:
                warns.append(f"{rel} 未被 SKILL.md 引用（孤儿文件）")

    # 4. 占位符
    for md in sorted(root.rglob("*.md")):
        if ".git" in md.parts:
            continue
        for i, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            if PLACEHOLDER_RE.search(line):
                warns.append(f"{md.relative_to(root)}:{i} 存在占位符：{line.strip()[:60]}")

    # 报告
    for w in warns:
        print(f"⚠ {w}")
    for e in errors:
        print(f"✗ {e}")

    files = [p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]
    md_count = len([p for p in files if p.suffix == ".md"])
    print(f"\n检查完成：{len(files)} 个文件（{md_count} 个 Markdown）"
          f" → {len(errors)} 个错误，{len(warns)} 个提醒")

    if errors:
        print("结果：FAIL")
        return 1
    print("结果：PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
