from __future__ import annotations

from pathlib import Path
from typing import List

from langchain_core.tools import tool

from pecko.core.paths import safe_path


@tool
def list_files(directory: str = ".") -> List[str]:
    """
    List entries in a workspace directory.

    Constraints:
    - `directory` must be a relative path within the workspace (no absolute paths, no ../).
    - Path must resolve to an existing directory.

    Returns:
    - Sorted List[str] of entries, prefixed with "[DIR]" or "[FILE]".
    - On error, returns a single-item list: ["Error: ..."].
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
    Read a UTF-8 text file from the workspace.

    Constraints:
    - Path must be relative to the workspace root.
    - File must exist and be text-based.

    Returns:
    - Full file contents as a string, or an error message.
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
    Create or overwrite a UTF-8 text file in the workspace.

    Constraints:
    - `file_path` must be a relative path within the workspace (no absolute paths, no ../).
    - Parent directories are created if missing.

    Returns:
    - Success message, or an "Error: ..." message.
    """
    try:
        target = safe_path(file_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

