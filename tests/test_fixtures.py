"""Test for the new fixtures."""

import io

from vws_test_fixtures.images import VWS_MAX_IMAGE_FILE_SIZE


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


def test_png_too_large_exceeds_vws_file_size_limit(
    png_too_large: io.BytesIO,
) -> None:
    """``png_too_large`` exceeds the VWS image file size limit."""
    assert len(png_too_large.getvalue()) > VWS_MAX_IMAGE_FILE_SIZE
