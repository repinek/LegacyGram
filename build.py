import os

# yes I videcoded this but works fine lol
# TODO uv version <version from header>

DIST_DIR = "dist"
OUTPUT_FILENAME = "LegacyGram.py"
SRC_DIR = "LegacyGram"

PRIORITY_FILES = ["header.py"]
PRIORITY_DIRS = ["data", "i18n", "utils"]
LAST_FILES = ["ui/settings.py", "main.py"]

COPYRIGHT_STRING = ("# Open Source LegacyGram plugin for https://exteragram.app\n"
                    "# Plugin created by t.me/wepinek\n"
                    "# Licensed under the MIT License\n"
                    "# Repository: https://github.com/repinek/LegacyGram\n")

def build():
    if not os.path.exists(DIST_DIR):
        os.makedirs(DIST_DIR)

    output_path = os.path.join(DIST_DIR, OUTPUT_FILENAME)
    final_content = []

    print(f"🚀 Starting build: {OUTPUT_FILENAME} from directory '{SRC_DIR}'...")

    if not os.path.exists(SRC_DIR):
        print(f"❌ Error: Source directory '{SRC_DIR}' not found!")
        return

    all_files = []
    files_to_process = []
    for root, dirs, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, SRC_DIR)
                all_files.append(rel_path.replace("\\", "/"))

    for file_name in PRIORITY_FILES:
        if file_name in all_files:
            files_to_process.append(file_name)
        else:
            print(f"⚠️ Warning: Priority file '{file_name}' not found in {SRC_DIR}.")

    for dir_name in PRIORITY_DIRS:
        prefix = dir_name.strip("/") + "/"
        dir_files = [
            file_name for file_name in all_files
            if (file_name.startswith(prefix) or file_name == dir_name)
               and file_name not in files_to_process
               and os.path.basename(file_name) != "__init__.py"
        ]
        if dir_files:
            dir_files.sort()
            files_to_process.extend(dir_files)
        else:
            print(f"⚠️ Warning: Priority directory '{dir_name}' is empty or not found in {SRC_DIR}.")

    for file_name in all_files:
        if (file_name not in PRIORITY_FILES and
                file_name not in LAST_FILES and
                file_name not in files_to_process and
                os.path.basename(file_name) != "__init__.py"):
            files_to_process.append(file_name)

    for file_name in LAST_FILES:
        if file_name in all_files:
            files_to_process.append(file_name)
        else:
            print(f"⚠️ Warning: Last file '{file_name}' not found in {SRC_DIR}.")

    print(f"📋 Merge order: {files_to_process}")

    for file_name in files_to_process:
        file_path = os.path.join(SRC_DIR, file_name)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            if not final_content:
                final_content.append(COPYRIGHT_STRING)
            final_content.append(f"\n# === CONTENT OF {file_name} ===\n")

            for line in lines:
                if "# @ignore" in line:
                    continue

                if file_name != "header.py":
                    stripped = line.strip()
                    if stripped.startswith("from ") or stripped.startswith("import "):
                        continue

                final_content.append(line)

            print(f"✅ Merged: {file_name}")

        except Exception as e:
            print(f"❌ Error reading {file_name}: {e}")
            return

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(final_content)

    print(f"\n🎉 Build successful! File saved to: {output_path}")


if __name__ == "__main__":
    build()