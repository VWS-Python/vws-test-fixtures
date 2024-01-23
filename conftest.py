"""Setup for Sybil."""

from doctest import ELLIPSIS

from sybil import Sybil
from sybil.parsers.rest import (
    CaptureParser,
    DocTestParser,
    PythonCodeBlockParser,
)

sybil_obj = Sybil(
    parsers=[
        DocTestParser(optionflags=ELLIPSIS),
        PythonCodeBlockParser(),
        CaptureParser(),
    ],
    patterns=["*.rst", "*.py"],
)

pytest_collect_file = sybil_obj.pytest()
