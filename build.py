import ast
import re
from pathlib import Path
from typing import List, Set
from collections import defaultdict

# TODO uv version <version from header>

"""
I don't love using vars like: a b c
but it's indeed here
p - path
f - file
pd - priority dir
"""

# CONFIGURATION
DIST_DIR = Path("dist")
OUTPUT_FILENAME = "LegacyGram.py"
SRC_DIR = Path("LegacyGram")

PRIORITY_FILES = ["header.py"]
PRIORITY_DIRS = ["data", "i18n", "utils"]
LAST_FILES = ["ui/settings.py", "main.py"]

COPYRIGHT_STRING = (
    "# Open Source LegacyGram plugin for https://exteragram.app\n"
    "# Plugin created by t.me/wepinek\n"
    "# Licensed under the MIT License\n"
    "# Repository: https://github.com/repinek/LegacyGram\n"
)

captured_imports = defaultdict(set)
captured_from_imports = defaultdict(set)

def get_all_python_files(src: Path) -> List[Path]:
    return [
        p.relative_to(src)
        for p in src.rglob("*.py")
        if p.name != "__init__.py"
    ]


def get_merge_order(all_files: List[Path]) -> List[Path]:
    order = []
    processed: Set[Path] = set()

    # Priority Files
    for pf in PRIORITY_FILES:
        p = Path(pf)
        if p in all_files:
            order.append(p)
            processed.add(p)

    # Priority Directories
    for pd in PRIORITY_DIRS:
        dir_files = sorted([
            f for f in all_files
            if f.parts[0] == pd and f not in processed
        ])
        order.extend(dir_files)
        processed.update(dir_files)

    # Everything else (except LAST_FILES)
    last_paths = {Path(f) for f in LAST_FILES}
    others = sorted([
        f for f in all_files
        if f not in processed and f not in last_paths
    ])
    order.extend(others)
    processed.update(others)

    # Last Files
    for lf in LAST_FILES:
        p = Path(lf)
        if p in all_files:
            order.append(p)
            processed.add(p)

    return order


def parse_import_line(line: str):
    line = line.strip()

    from_match = re.match(r"^from ([\w.]+) import (.+)$", line)
    if from_match:
        module, names = from_match.groups()
        for name in names.split(","):
            captured_from_imports[module].add(name.strip())
        return

    import_match = re.match(r"^import ([\w.]+)$", line)
    if import_match:
        module = import_match.group(1)
        _ = captured_imports[module]


def generate_imports_block() -> str:
    lines = []

    for mod in sorted(captured_imports.keys()):
        lines.append(f"import {mod}")

    for mod in sorted(captured_from_imports.keys()):
        names = sorted(list(captured_from_imports[mod]))
        lines.append(f"from {mod} import {', '.join(names)}")

    return "\n".join(lines) + "\n"


def process_file_content(file_path: Path) -> List[str]:
    """ Removes imports and @ignore lines """
    processed_lines = []

    with open(SRC_DIR / file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        stripped = line.strip()

        if "# @ignore" in line:
            continue

        is_import = stripped.startswith(("import ", "from "))
        is_internal = stripped.startswith(("import LegacyGram", "from LegacyGram", "from ."))

        if is_import:
            if not is_internal:
                parse_import_line(stripped)
            continue

        processed_lines.append(line)

    file_code = "".join(processed_lines)

    try:
        ast.parse(file_code)
    except SyntaxError as e:
        raise SyntaxError(f"❌ Syntax Error in file: {file_path} line {e.lineno}: {e.msg}") from e

    return processed_lines


def build():
    print(f"🚀 Starting build: {OUTPUT_FILENAME}...")

    if not SRC_DIR.exists():
        print(f"❌ Error: Source directory '{SRC_DIR}' not found!")
        return

    all_files = get_all_python_files(SRC_DIR)
    merge_order = get_merge_order(all_files)

    body_content = []
    for file_path in merge_order:
        print(f"📦 Merging: {file_path}")
        body_content.append(f"\n# === {file_path} ===\n")
        body_content.extend(process_file_content(file_path))

    imports_block = generate_imports_block()
    full_code = COPYRIGHT_STRING + "\n" + imports_block + "".join(body_content)

    DIST_DIR.mkdir(exist_ok=True)
    out_path = DIST_DIR / OUTPUT_FILENAME
    out_path.write_text(full_code, encoding="utf-8")

    print(f"\n🎉 Build successful: {out_path}")


if __name__ == "__main__":
    build()