"""Fixtures for mock Vuforia databases.

These fixtures require the optional ``mock`` extra::

    pip install 'vws-test-fixtures[mock]'

That extra depends on ``vws-python-mock``, which requires Python 3.14+.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Generator

    from mock_vws.database import CloudDatabase, VuMarkDatabase


def _ensure_mock_vws() -> None:
    """Raise a clear install error when ``mock_vws`` is missing."""
    try:
        import mock_vws  # noqa: F401
    except ImportError as exc:
        message = (
            "Database fixtures need the optional 'mock' extra: "
            "pip install 'vws-test-fixtures[mock]'"
        )
        raise ImportError(message) from exc


@dataclass(frozen=True, kw_only=True)
class ModelTargetCredentials:
    """OAuth2 client credentials accepted by ``mock_vws`` by default.

    These match the fixed Model Target credentials built into
    ``vws-python-mock``. Use them with ``MockVWS`` active (for example via
    the ``mock_model_target_credentials`` fixture).
    """

    client_id: str = "client-id"
    client_secret: str = "client-secret"


@pytest.fixture(name="mock_cloud_database")
def fixture_mock_cloud_database() -> Generator[CloudDatabase]:
    """Yield a ``CloudDatabase`` served by ``MockVWS``.

    The database uses randomly generated server and client keys (the
    standard ``CloudDatabase`` defaults). Processing time is kept low so
    tests run quickly.
    """
    _ensure_mock_vws()
    from mock_vws import MockVWS
    from mock_vws.database import CloudDatabase

    with MockVWS(processing_time_seconds=0.2) as mock:
        database = CloudDatabase()
        mock.add_cloud_database(cloud_database=database)
        yield database


@pytest.fixture(name="mock_vumark_database")
def fixture_mock_vumark_database() -> Generator[VuMarkDatabase]:
    """Yield a ``VuMarkDatabase`` with one template target, served by
    ``MockVWS``.
    """
    _ensure_mock_vws()
    from mock_vws import MockVWS
    from mock_vws.database import VuMarkDatabase
    from mock_vws.target import VuMarkTarget

    vumark_target = VuMarkTarget(name="vumark-template")
    with MockVWS() as mock:
        database = VuMarkDatabase(vumark_targets={vumark_target})
        mock.add_vumark_database(vumark_database=database)
        yield database


@pytest.fixture(name="mock_model_target_credentials")
def fixture_mock_model_target_credentials() -> Generator[
    ModelTargetCredentials
]:
    """Yield Model Target OAuth2 credentials while ``MockVWS`` is active.

    ``mock_vws`` does not expose a separate Model Target database type;
    these are the fixed client credentials the mock accepts for the Model
    Target Web API.
    """
    _ensure_mock_vws()
    from mock_vws import MockVWS

    credentials = ModelTargetCredentials()
    with MockVWS(processing_time_seconds=0.2):
        yield credentials
