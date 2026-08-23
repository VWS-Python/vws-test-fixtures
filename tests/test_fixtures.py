"""Test for the new fixtures."""

import io

from vws_test_fixtures.images import _bytes_io, _load_resource_bytes


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


def test_bytes_io_handles_are_independent() -> None:
    """Fresh ``BytesIO`` handles share bytes but not read position."""
    data = _load_resource_bytes(name="high_quality_image.jpg")
    first = _bytes_io(data=data)
    second = _bytes_io(data=data)
    assert first.read() == data
    assert first.tell() == len(data)
    assert second.tell() == 0
    assert second.read() == data
