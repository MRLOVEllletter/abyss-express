import os
import re

INTERNAL_MODULES = ["engine.", "player.", "data.", "train.", "dungeons."]

FILES = [
    "engine/display.py",
    "player/player.py",
    "data/items.py",
    "train/train.py",
    "dungeons/town.py",
    "main.py"
]


def is_internal_import(line):
    stripped = line.strip()
    if stripped.startswith("from ") or stripped.startswith("import "):
        for mod in INTERNAL_MODULES:
            if mod in stripped:
                return True
    return False


def bundle(output="game_web.py"):
    lines = []
    lines.append("# 深渊列车 · Abyss Express — Web Bundle")
    lines.append("import sys, time, random")
    lines.append("")

    for f in FILES:
        path = os.path.join(os.path.dirname(__file__), f)
        with open(path, encoding="utf-8") as fh:
            content = fh.read()

        cleaned_lines = []
        for line in content.split("\n"):
            if is_internal_import(line):
                continue
            if f == "main.py" and line.strip().startswith("if __name__"):
                cleaned_lines.append("# [web] auto-start: game entry")
                cleaned_lines.append("set_slow(True)")
                cleaned_lines.append("main()")
                continue
            if f == "main.py" and line.strip().startswith("main()") and not line.strip().startswith("#"):
                continue
            cleaned_lines.append(line)

        lines.append(f"# === {f} ===")
        lines.extend(cleaned_lines)
        lines.append("")

    full = "\n".join(lines)

    out_path = os.path.join(os.path.dirname(__file__), output)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(full)

    line_count = full.count("\n")
    print(f"✅ Bundled {len(FILES)} files -> {output}")
    print(f"   Lines: {line_count}, Chars: {len(full)}")


if __name__ == "__main__":
    bundle()