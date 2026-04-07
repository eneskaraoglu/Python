"""
patch_turkish.py

Fixes lost Turkish characters in Project1 (UTF-8) by copying correct lines
from Project2 (original Cp1254).

How it works:
  - Walks Project2 recursively
  - For each file, reads it line by line (as Cp1254)
  - Finds lines that contain Turkish characters
  - Opens the matching file in Project1 (UTF-8)
  - Replaces those lines in Project1 with the correct UTF-8 version
  - Saves Project1 file (with a .bak backup first)

Usage:
  python patch_turkish.py <project1_dir> <project2_dir> [--dry-run]

Example:
  python patch_turkish.py C:/projects/erp_utf8 C:/projects/erp_original --dry-run
  python patch_turkish.py C:/projects/erp_utf8 C:/projects/erp_original
"""

import os
import sys
import shutil

# Turkish-specific characters
TURKISH_CHARS = set("şğıöüçŞĞİÖÜÇ")

# File extensions to process
TARGET_EXTENSIONS = {".java", ".xml", ".properties", ".sql"}

# Stats
stats = {"patched": 0, "skipped": 0, "failed": 0, "lines_fixed": 0}


def has_turkish(text: str) -> bool:
    return any(c in TURKISH_CHARS for c in text)


def patch_file(p1_path: str, p2_path: str, dry_run: bool):
    """
    Compare files line by line.
    For every line in Project2 that has Turkish chars,
    replace the corresponding line in Project1.
    """
    try:
        # Read Project2 (original Cp1254) → decode to proper Unicode
        with open(p2_path, "r", encoding="cp1254", errors="replace") as f:
            p2_lines = f.readlines()

        # Read Project1 (broken UTF-8)
        with open(p1_path, "r", encoding="utf-8", errors="replace") as f:
            p1_lines = f.readlines()

        if len(p1_lines) != len(p2_lines):
            print(f"[WARN] Line count mismatch: {p1_path}")
            print(f"       Project1={len(p1_lines)} lines, Project2={len(p2_lines)} lines")
            print(f"       Will patch only matching line numbers.")

        fixed_lines = list(p1_lines)  # start with Project1 content
        lines_fixed = 0
        min_lines = min(len(p1_lines), len(p2_lines))

        for i in range(min_lines):
            p2_line = p2_lines[i]
            if has_turkish(p2_line):
                # Replace Project1 line with correct UTF-8 line from Project2
                fixed_lines[i] = p2_line
                lines_fixed += 1

        if lines_fixed == 0:
            print(f"[SKIP]  {p1_path}  (no Turkish chars found)")
            stats["skipped"] += 1
            return

        if dry_run:
            print(f"[PATCH] {p1_path}  → {lines_fixed} line(s) would be fixed  (dry-run)")
            stats["patched"] += 1
            stats["lines_fixed"] += lines_fixed
            return

        # Backup Project1 file before overwriting
        backup_path = p1_path + ".bak"
        shutil.copy2(p1_path, backup_path)

        # Write fixed content back to Project1 as UTF-8
        with open(p1_path, "w", encoding="utf-8") as f:
            f.writelines(fixed_lines)

        print(f"[PATCH] {p1_path}  → {lines_fixed} line(s) fixed  (backup: {os.path.basename(backup_path)})")
        stats["patched"] += 1
        stats["lines_fixed"] += lines_fixed

    except Exception as e:
        print(f"[FAIL]  {p1_path}  — {e}")
        stats["failed"] += 1


def run(project1: str, project2: str, dry_run: bool):
    print(f"Project1 (UTF-8, broken) : {os.path.abspath(project1)}")
    print(f"Project2 (Cp1254, original): {os.path.abspath(project2)}")
    if dry_run:
        print("=== DRY RUN — no files will be changed ===")
    print("-" * 60)

    # Walk Project2 as the reference
    for root, dirs, files in os.walk(project2):
        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext not in TARGET_EXTENSIONS:
                continue

            p2_path = os.path.join(root, filename)

            # Build the matching path in Project1
            relative_path = os.path.relpath(p2_path, project2)
            p1_path = os.path.join(project1, relative_path)

            if not os.path.exists(p1_path):
                print(f"[MISSING] {p1_path}  (not found in Project1, skipping)")
                stats["skipped"] += 1
                continue

            patch_file(p1_path, p2_path, dry_run)

    print("-" * 60)
    print(f"Done.")
    print(f"  Files patched : {stats['patched']}")
    print(f"  Lines fixed   : {stats['lines_fixed']}")
    print(f"  Files skipped : {stats['skipped']}")
    print(f"  Files failed  : {stats['failed']}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python patch_turkish.py <project1_dir> <project2_dir> [--dry-run]")
        sys.exit(1)

    project1_dir = sys.argv[1]
    project2_dir = sys.argv[2]
    dry_run_mode = len(sys.argv) > 3 and sys.argv[3] == "--dry-run"

    if not os.path.isdir(project1_dir):
        print(f"ERROR: Project1 directory not found: {project1_dir}")
        sys.exit(1)

    if not os.path.isdir(project2_dir):
        print(f"ERROR: Project2 directory not found: {project2_dir}")
        sys.exit(1)

    run(project1_dir, project2_dir, dry_run_mode)