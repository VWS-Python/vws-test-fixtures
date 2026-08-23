"""Setup for Sybil and optional mock tests."""

from __future__ import annotations

import importlib.util
from doctest import ELLIPSIS
from typing import TYPE_CHECKING

from sybil import Sybil
from sybil.parsers.rest import (
    DocTestParser,
    PythonCodeBlockParser,
)

if TYPE_CHECKING:
    from pathlib import Path

    import pytest

sybil = Sybil(
    parsers=[
        DocTestParser(optionflags=ELLIPSIS),
        PythonCodeBlockParser(),
    ],
    patterns=["*.rst", "*.py"],
)

pytest_collect_file = sybil.pytest()


def pytest_ignore_collect(
    collection_path: Path,
    config: pytest.Config,
) -> bool:
    """Skip collecting mock database tests without ``mock_vws``.

    Those tests need the optional ``mock`` extra (Python 3.14+). Ignoring
    the file keeps ``test_databases.py`` free of skip/import tricks.
    """
    del config
    if collection_path.name != "test_databases.py":
        return False
    return importlib.util.find_spec(name="mock_vws") is None
