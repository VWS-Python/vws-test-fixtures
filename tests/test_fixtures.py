"""Test for the new fixtures."""

import io
from pathlib import Path


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


def test_image_path_fixtures(
    *,
    high_quality_image: io.BytesIO,
    high_quality_image_path: Path,
    different_high_quality_image: io.BytesIO,
    different_high_quality_image_path: Path,
) -> None:
    """Path fixtures write fixture bytes to temporary files."""
    assert high_quality_image_path.is_file()
    assert (
        high_quality_image_path.read_bytes() == high_quality_image.getvalue()
    )
    assert different_high_quality_image_path.is_file()
    assert (
        different_high_quality_image_path.read_bytes()
        == different_high_quality_image.getvalue()
    )
