"""Setup for Sybil."""

from doctest import ELLIPSIS

from sybil import (  # pyright: ignore [reportMissingTypeStubs]
    Sybil,
)
from sybil.parsers.rest import (  # pyright: ignore [reportMissingTypeStubs]
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

pytest_collect_file = (  # pyright: ignore [reportUnknownVariableType]
    sybil_obj.pytest()  # pyright: ignore [reportUnknownMemberType]
)
