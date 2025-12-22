from __future__ import annotations

from pathlib import Path
from typing import List

from langchain_core.tools import tool

from pecko.core.paths import safe_path


@tool
def list_files(directory: str = ".") -> List[str]:
    """
List files and directories inside a workspace directory.

Purpose:
    Use this tool to explore the project structure or discover files
    before reading or modifying them.

Path Rules:
    - `directory` must be a path relative to the workspace root.
    - Absolute paths and path traversal (e.g. '../') are not allowed.
    - The path must resolve to a directory.

Behavior:
    - Returns a sorted list of entries in the directory.
    - Each entry is prefixed with:
        '[DIR] '  for directories
        '[FILE]' for files

Returns:
    - List[str]: One entry per file or directory.
    - On error, returns a list with a single error message.

Typical Usage:
    - Inspect repository layout
    - Find files to read or edit
    - Confirm file creation or deletion

Example Output:
    [
        "[DIR] src",
        "[FILE] README.md",
        "[FILE] pyproject.toml"
    ]
    """
    try:
        target_dir = safe_path(directory)
        if not target_dir.is_dir():
            return [f"Error: {directory} is not a directory"]
        
        items = []
        for item in target_dir.iterdir():
            prefix = "[DIR] " if item.is_dir() else "[FILE]"
            items.append(f"{prefix} {item.name}")
        
        return sorted(items)
    except Exception as e:
        return [f"Error: {str(e)}"]


@tool
def read_file(file_path: str) -> str:
    """
    Read the full text contents of a file in the workspace.

    Purpose:
        Use this tool to inspect source code, configuration files,
        documentation, or other text-based files before reasoning
        or making changes.

    File Type Constraints:
        - Intended for text files only (e.g. .py, .md, .html, .json, .c, .etc).
        - Not suitable for binary files (e.g. images, PDFs, archives).

    Path Rules:
        - `file_path` must be relative to the workspace root.
        - Absolute paths and path traversal are not allowed.
        - The path must resolve to an existing file.

    Behavior:
        - Reads the entire file as UTF-8 text.
        - Returns the raw file contents as a string.

    Returns:
        - str: Full file contents.
        - On error, returns a descriptive error message.

    Typical Usage:
        - Inspect code before editing
        - Understand existing logic
        - Review configuration or documentation

    Failure Notes:
        - Large files may be rejected by higher-level logic.
        - Binary or non-UTF8 files may produce errors.
    """
    try:
        target = safe_path(file_path)
        if not target.is_file():
            return f"Error: {file_path} is not a file or does not exist."
        
        return target.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def write_file(file_path: str, content: str) -> str:
    """
    Create or overwrite a text file in the workspace.

    Purpose:
        Use this tool to create new files or replace the contents
        of existing text-based files such as source code,
        documentation, or configuration files.

    File Type Constraints:
        - Intended for text files only (UTF-8).
        - Not suitable for binary files.

    Path Rules:
        - `file_path` must be relative to the workspace root.
        - Absolute paths and path traversal are not allowed.
        - Parent directories will be created automatically if needed.

    Behavior:
        - Overwrites the file if it already exists.
        - Creates the file if it does not exist.
        - Writes content using UTF-8 encoding.

    Returns:
        - str: Success confirmation message.
        - On error, returns a descriptive error message.

    Typical Usage:
        - Write new source code files
        - Apply full-file refactors
        - Generate documentation
        - Update configuration files
    """
    try:
        target = safe_path(file_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

