"""Fixtures automatically available when this plugin is installed."""

from __future__ import annotations

pytest_plugins: list[str] = [
    "vws_test_fixtures.images",
    "vws_test_fixtures.databases",
]
