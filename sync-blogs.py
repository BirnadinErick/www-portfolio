#!/usr/bin/env python3
import argparse
import shutil
import sys
from pathlib import Path

CONFIG_NAME = ".blogdirs"


def read_config(config_file: Path) -> tuple[Path | None, Path | None]:
    """Read saved source and dest paths from config file."""
    if not config_file.exists():
        return None, None

    saved_source = None
    saved_dest = None

    try:
        lines = config_file.read_text(encoding="utf-8").splitlines()
        for line in lines:
            if line.startswith("SOURCE="):
                saved_source = Path(line.split("=", 1)[1]).expanduser().resolve()
            elif line.startswith("DEST="):
                saved_dest = Path(line.split("=", 1)[1]).expanduser().resolve()
    except Exception as e:
        print(f"Warning: Could not read '{config_file.name}': {e}")

    return saved_source, saved_dest


def save_config(config_file: Path, source_path: Path, dest_path: Path) -> None:
    """Save source and dest paths to config file."""
    try:
        content = f"SOURCE={source_path}\nDEST={dest_path}\n"
        config_file.write_text(content, encoding="utf-8")
        print(f"Saved configuration to '{config_file.name}'.")
    except Exception as e:
        print(f"Warning: Failed to write to '{config_file.name}': {e}")


def main():
    parser = argparse.ArgumentParser(
        description=f"Copy Markdown files from a source directory to a target directory, saving paths in {CONFIG_NAME}."
    )
    parser.add_argument(
        "source_dir",
        type=str,
        nargs="?",
        default=None,
        help=f"Path to source directory. If omitted, loads from {CONFIG_NAME}.",
    )
    parser.add_argument(
        "dest_dir",
        type=str,
        nargs="?",
        default=None,
        help=f"Path to target directory. If omitted, loads from {CONFIG_NAME}.",
    )
    parser.add_argument(
        "--config",
        "-c",
        type=str,
        default=CONFIG_NAME,
        help=f"Config file to save/read directory paths (default: {CONFIG_NAME}).",
    )

    args = parser.parse_args()
    config_file = Path(args.config)

    # Load existing saved paths
    saved_source, saved_dest = read_config(config_file)

    # Resolve source path
    if args.source_dir:
        source_path = Path(args.source_dir).expanduser().resolve()
    elif saved_source:
        source_path = saved_source
        print(f"Using saved source directory from '{config_file.name}'.")
    else:
        print(
            f"Error: No source directory specified and none found in '{config_file.name}'."
        )
        sys.exit(1)

    # Resolve target path
    if args.dest_dir:
        dest_path = Path(args.dest_dir).expanduser().resolve()
    elif saved_dest:
        dest_path = saved_dest
        print(f"Using saved target directory from '{config_file.name}'.")
    elif args.source_dir:
        # Default target if source is supplied for the first time
        dest_path = Path("blog_posts").expanduser().resolve()
    else:
        print(
            f"Error: No target directory specified and none found in '{config_file.name}'."
        )
        sys.exit(1)

    # Validate source path
    if not source_path.exists():
        print(f"Error: Source directory '{source_path}' does not exist.")
        sys.exit(1)
    if not source_path.is_dir():
        print(f"Error: '{source_path}' is not a directory.")
        sys.exit(1)

    print(f"Source Directory: {source_path}")
    print(f"Target Directory: {dest_path}")

    # Save current choices to config file
    save_config(config_file, source_path, dest_path)

    # Ensure target directory exists
    dest_path.mkdir(parents=True, exist_ok=True)

    # Find and copy all .md and .markdown files
    markdown_files = list(source_path.glob("*.md")) + list(
        source_path.glob("*.markdown")
    )

    if not markdown_files:
        print(f"No Markdown files found in '{source_path}'.")
        return

    copied_count = 0
    for file_path in markdown_files:
        if file_path.is_file():
            shutil.copy2(file_path, dest_path / file_path.name)
            copied_count += 1
            print(f"Copied: {file_path.name}")

    print(f"\nSuccessfully copied {copied_count} file(s) to '{dest_path}'.")


if __name__ == "__main__":
    main()
