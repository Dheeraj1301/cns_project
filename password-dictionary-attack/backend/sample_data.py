"""Data loading helpers for the educational demo."""

from pathlib import Path
from typing import List


def load_default_dictionary() -> List[str]:
    """Load the built-in sample dictionary from the project directory."""
    project_root = Path(__file__).resolve().parent.parent
    dictionary_path = project_root / "dictionaries" / "sample_dictionary.txt"

    if not dictionary_path.exists():
        raise FileNotFoundError(f"Dictionary file not found: {dictionary_path}")

    words = [line.strip() for line in dictionary_path.read_text(encoding="utf-8").splitlines()]
    return [word for word in words if word]
