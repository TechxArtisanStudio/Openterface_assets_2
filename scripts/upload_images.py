#!/usr/bin/env python3
"""
Upload images from a source folder to src/images/, detect target subdirectory
by filename, handle duplicates, generate URLs, and output a markdown file
with the new links.

Usage:
    python3 scripts/upload_images.py /path/to/image/folder
    python3 scripts/upload_images.py /path/to/image/folder --output links/new-links.md
"""

import os
import sys
import shutil
import argparse
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib

PROJECT_ROOT = Path(__file__).parent.parent
SRC_IMAGES = PROJECT_ROOT / "src" / "images"
DEFAULT_BASE_URL = "https://assets2.openterface.com"

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp"}
WEBP_CONVERT_EXTENSIONS = {".png", ".jpg", ".jpeg"}

# Subdirectory mapping: keyword → subdir name (checked in order)
SUBDIR_RULES = [
    ("kvm-go", "kvm-go"),
    ("keymod", "keymod"),
    ("km-", "keymod"),      # KM-Basic, KM-Pro → keymod/
    ("gamepad", "keymod"),   # KeyMod gamepad presets → keymod/
    ("icon", "icon"),
    ("blog", "blog"),
]


def load_config() -> dict:
    config_path = PROJECT_ROOT / "config.toml"
    if config_path.exists():
        with open(config_path, "rb") as f:
            config = tomllib.load(f)
        return config.get("repository", {}).get("base_url", DEFAULT_BASE_URL)
    return DEFAULT_BASE_URL


def get_target_subdir(filename: str) -> str:
    """Determine target subdirectory based on filename."""
    lower = filename.lower()
    for keyword, subdir in SUBDIR_RULES:
        if keyword in lower:
            return subdir
    return ""  # root


def resolve_unique_path(target_dir: Path, filename: str) -> str:
    """Return a unique filename, appending _N if needed."""
    dest = target_dir / filename
    if not dest.exists():
        return filename

    stem = Path(filename).stem
    suffix = Path(filename).suffix
    n = 1
    while True:
        new_name = f"{stem}_{n}{suffix}"
        if not (target_dir / new_name).exists():
            return new_name
        n += 1


def upload_images(source: Path, base_url: str) -> tuple[list[dict], list[str]]:
    """Copy images and return (results, skipped)."""
    results = []
    skipped = []

    if source.is_dir():
        files = sorted([
            f for f in source.iterdir()
            if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
        ])
    else:
        # Single file
        if source.suffix.lower() in IMAGE_EXTENSIONS:
            files = [source]
        else:
            return [], [source.name]

    if not files:
        print(f"No valid images found in {source}")
        return results, skipped

    for src_file in files:
        subdir = get_target_subdir(src_file.name)
        target_dir = SRC_IMAGES / subdir if subdir else SRC_IMAGES
        target_dir.mkdir(parents=True, exist_ok=True)

        final_name = resolve_unique_path(target_dir, src_file.name)
        dest_path = target_dir / final_name

        shutil.copy2(src_file, dest_path)

        # Build URL
        url_path = f"images/{subdir}/" if subdir else "images/"

        # For PNG/JPG/JPEG, the build converts to .webp
        if src_file.suffix.lower() in WEBP_CONVERT_EXTENSIONS:
            url_name = Path(final_name).stem + ".webp"
        else:
            url_name = final_name

        url = f"{base_url}/{url_path}{url_name}"

        renamed_note = f" (renamed from {src_file.name})" if final_name != src_file.name else ""

        results.append({
            "original": src_file.name,
            "final": final_name,
            "subdir": subdir or "(root)",
            "url": url,
            "renamed": renamed_note,
        })

    return results, skipped


def write_markdown_output(results: list[dict], output_path: Path):
    """Write a clean markdown file with the new image links (both markdown and HTML img)."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# New Image Links\n\n")
        f.write("## Markdown Links\n\n")
        f.write("Copy and paste these links into your markdown files:\n\n")

        for r in results:
            name = Path(r["final"]).stem
            f.write(f"[{name}]({r['url']})\n\n")

        f.write("---\n\n## HTML Image Tags\n\n")
        f.write("Copy and paste these into your website HTML:\n\n")

        for r in results:
            alt = Path(r["final"]).stem
            f.write(f'<img src="{r["url"]}" alt="{alt}" />\n\n')


def print_summary(results: list[dict], skipped: list[str], output_path: Path):
    """Print summary table to stdout."""
    print(f"\nUploaded {len(results)} image(s) to Openterface_assets_2:\n")
    print(f"| Original File | Final Name | URL |")
    print(f"|---|---|---|")

    for r in results:
        final_display = r["final"]
        if r["renamed"]:
            final_display = r["final"] + r["renamed"]
        print(f"| {r['original']} | {final_display} | {r['url']} |")

    if skipped:
        print(f"\nSkipped {len(skipped)} non-image file(s): {', '.join(skipped)}")

    print(f"\nMarkdown links written to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Upload images to Openterface assets repo")
    parser.add_argument("source", type=str, help="Path to image folder or single image file")
    parser.add_argument("--output", type=str, default=None,
                        help="Output markdown file path (default: links/new-<timestamp>.md)")
    args = parser.parse_args()

    source = Path(args.source).resolve()
    if not source.exists():
        print(f"Error: {source} does not exist")
        sys.exit(1)

    # Handle single file vs directory
    if source.is_file():
        if source.suffix.lower() not in IMAGE_EXTENSIONS:
            print(f"Error: {source.name} is not a supported image format")
            sys.exit(1)
        # Treat single file as a "folder" with one file
        files = [source]
        source_dir = source.parent
    elif source.is_dir():
        pass  # will iterate inside upload_images
    else:
        print(f"Error: {source} is not a file or directory")
        sys.exit(1)

    base_url = load_config()
    print(f"Base URL: {base_url}")
    print(f"Source: {source}")

    # Run upload
    results, skipped = upload_images(source, base_url)

    if not results:
        sys.exit(0)

    # Determine output path
    if args.output:
        output_path = Path(args.output).resolve()
    else:
        import datetime
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        output_path = PROJECT_ROOT / "links" / f"new-links-{ts}.md"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write markdown
    write_markdown_output(results, output_path)

    # Print summary
    print_summary(results, skipped, output_path)

    # Output for downstream consumption (commit message)
    filenames = ", ".join([r["final"] for r in results])
    print(f"\n--COMMIT-MSG-- add images: {filenames}")


if __name__ == "__main__":
    main()
