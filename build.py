import ast
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

"""
I don't love using vars like: a b c
but it's really needed here
p - path
f - file
pd - priority dir
"""

# CONFIGURATION
DIST_DIR = Path("dist")
OUTPUT_FILENAME = "LegacyGram.plugin"
SRC_DIR = Path("LegacyGram")
HEADER_FILE = SRC_DIR / "header.py"

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


def get_current_version() -> tuple[int, int, int] | None:
    content = HEADER_FILE.read_text(encoding="utf-8")
    match = re.search(r'__version__\s*=\s*"(\d+)\.(\d+)\.(\d+)"', content)
    if match:
        return int(match.group(1)), int(match.group(2)), int(match.group(3))
    print("❌ Error: Can't find version!")
    return None


def increment_build_version(current_version: tuple[int, int, int]) -> str:
    major, minor, build = current_version
    new_version = (major, minor, build + 1)

    version_str = f"{new_version[0]}.{new_version[1]}.{new_version[2]}"

    # Update header.py
    content = HEADER_FILE.read_text(encoding="utf-8")
    content = re.sub(
        r'__version__\s*=\s*"[^"]+"',
        f'__version__ = "{version_str}"',
        content,
    )
    HEADER_FILE.write_text(content, encoding="utf-8")

    return version_str


def run_linter():
    print("🔍 Running Ruff...")

    subprocess.run(["ruff", "check", ".", "--fix"], capture_output=True)
    subprocess.run(["ruff", "format", "."], capture_output=True)

    result = subprocess.run(["ruff", "check", "."], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Issues found:\n{result.stdout}")
        return False

    print("✅ Code is clean. Proceeding to build...")
    return True


def get_all_python_files(src: Path) -> list[Path]:
    return [p.relative_to(src) for p in src.rglob("*.py") if p.name != "__init__.py"]


def get_merge_order(all_files: list[Path]) -> list[Path]:
    order = []
    processed: set[Path] = set()

    # Priority Files
    for pf in PRIORITY_FILES:
        p = Path(pf)
        if p in all_files:
            order.append(p)
            processed.add(p)

    # Priority Directories
    for pd in PRIORITY_DIRS:
        dir_files = sorted([f for f in all_files if f.parts[0] == pd and f not in processed])
        order.extend(dir_files)
        processed.update(dir_files)

    # Everything else (except LAST_FILES)
    last_paths = {Path(f) for f in LAST_FILES}
    others = sorted([f for f in all_files if f not in processed and f not in last_paths])
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
        names = sorted(captured_from_imports[mod])
        lines.append(f"from {mod} import {', '.join(names)}")

    return "\n".join(lines) + "\n"


def process_file_content(file_path: Path) -> list[str]:
    """Removes imports and @ignore lines"""
    processed_lines = []

    with open(SRC_DIR / file_path, encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        stripped = line.strip()

        if "# @ignore" in line:
            continue

        is_import = stripped.startswith(("import ", "from "))
        is_internal = stripped.startswith(("import LegacyGram", "from LegacyGram"))

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

    cleaned_code = file_code.strip()
    cleaned_code = re.sub(r"\n{3,}", "\n\n", cleaned_code)

    return [cleaned_code + "\n"]


def build():
    print(f"🚀 Starting build: {OUTPUT_FILENAME}...")

    if not SRC_DIR.exists():
        print(f"❌ Error: Source directory '{SRC_DIR}' not found!")
        return

    if not HEADER_FILE.exists():
        print(f"❌ Error: Header file '{HEADER_FILE}' not found!")
        return

    current_version = get_current_version()
    if not current_version:
        print("❌ Error: Can't find __version__ field in header!")
        return

    new_version = increment_build_version(current_version)
    print(f"📌 Version: {new_version}")

    if not run_linter():
        sys.exit(1)

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
