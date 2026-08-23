"""Fixtures for application metadata."""

import base64

import pytest

# Vuforia maximum decoded application metadata size in bytes.
_MAX_METADATA_BYTES = 1024 * 1024 - 1


@pytest.fixture
def application_metadata_near_size_limit() -> str:
    """Base64-encoded application metadata near the VWS decoded size limit.

    The decoded payload is exactly ``1024 * 1024 - 1`` bytes, which is the
    maximum accepted by Vuforia. The returned value is suitable for the
    ``application_metadata`` request field.
    """
    return base64.b64encode(s=b"a" * _MAX_METADATA_BYTES).decode(
        encoding="ascii",
    )
