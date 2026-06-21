#!/usr/bin/env python3
"""
Fix encoding for all text files in the skill.

Converts all .md, .yaml, .py files to UTF-8.
"""
from pathlib import Path
import sys

def fix_encoding(file_path):
    """Try to read file and convert to UTF-8."""
    try:
        # Try UTF-8 first
        content = file_path.read_text(encoding="utf-8")
        return True, "already UTF-8"
    except UnicodeDecodeError:
        # Try GBK
        try:
            content = file_path.read_text(encoding="gbk")
            file_path.write_text(content, encoding="utf-8")
            return True, "converted from GBK"
        except:
            try:
                # Try latin-1 as last resort
                content = file_path.read_text(encoding="latin-1")
                file_path.write_text(content, encoding="utf-8")
                return True, "converted from latin-1"
            except:
                return False, "failed"

def main():
    skill_dir = Path(__file__).parent.parent
    patterns = ["**/*.md", "**/*.yaml", "**/*.py"]

    fixed = []
    failed = []

    for pattern in patterns:
        for file_path in skill_dir.glob(pattern):
            if file_path.is_file():
                success, msg = fix_encoding(file_path)
                if success and msg != "already UTF-8":
                    fixed.append((file_path, msg))
                    print(f"OK {file_path.relative_to(skill_dir)}: {msg}")
                elif not success:
                    failed.append(file_path)
                    print(f"FAIL {file_path.relative_to(skill_dir)}: {msg}")

    print(f"\nFixed: {len(fixed)}")
    print(f"Failed: {len(failed)}")

    if failed:
        sys.exit(1)

if __name__ == "__main__":
    main()
