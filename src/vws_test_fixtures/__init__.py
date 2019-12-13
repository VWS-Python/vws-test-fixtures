"""
``pytest`` fixtures for testing Vuforia Web Services related tools.
"""

from ._version import get_versions

__version__ = get_versions()['version']  # type: ignore
del get_versions
