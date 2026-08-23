"""Test for the new fixtures."""

import base64
import io

_MAX_METADATA_BYTES = 1024 * 1024 - 1


def test_image_fixtures(
    *,
    high_quality_image: io.BytesIO,
    image_file_failed_state: io.BytesIO,
    png_too_large: io.BytesIO,
    image_file_success_state_low_rating: io.BytesIO,
    corrupted_image_file: io.BytesIO,
    image_files_failed_state: io.BytesIO,
    bad_image_file: io.BytesIO,
    different_high_quality_image: io.BytesIO,
) -> None:
    """The image functions can be used as fixtures."""
    fixture_bytes_list = [
        high_quality_image.getvalue(),
        image_file_failed_state.getvalue(),
        png_too_large.getvalue(),
        image_file_success_state_low_rating.getvalue(),
        corrupted_image_file.getvalue(),
        image_files_failed_state.getvalue(),
        bad_image_file.getvalue(),
        different_high_quality_image.getvalue(),
    ]
    assert len(set(fixture_bytes_list)) == len(fixture_bytes_list)


def test_application_metadata_near_size_limit(
    *,
    application_metadata_near_size_limit: str,
) -> None:
    """Metadata decodes to the maximum allowed number of bytes."""
    decoded = base64.b64decode(
        s=application_metadata_near_size_limit.encode(encoding="ascii"),
    )
    assert len(decoded) == _MAX_METADATA_BYTES
