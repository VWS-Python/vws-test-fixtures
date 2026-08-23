"""Test for the new fixtures."""

import io

from PIL import Image

# Mirrors limits used by the fixtures under test.
_MAX_TARGET_IMAGE_BYTES = 2_359_293
_MAX_QUERY_IMAGE_BYTES = 2 * 1024 * 1024
_MAX_IMAGE_PIXELS = 37_748_736


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
    jpeg_too_large: io.BytesIO,
    pixel_count_too_large: io.BytesIO,
    png_just_under_max_size: io.BytesIO,
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
        jpeg_too_large.getvalue(),
        pixel_count_too_large.getvalue(),
        png_just_under_max_size.getvalue(),
    ]
    assert len(set(fixture_bytes_list)) == len(fixture_bytes_list)


def test_jpeg_too_large(*, jpeg_too_large: io.BytesIO) -> None:
    """The JPEG exceeds the Cloud Recognition query size limit."""
    assert len(jpeg_too_large.getvalue()) > _MAX_QUERY_IMAGE_BYTES
    with Image.open(fp=jpeg_too_large) as image:
        assert image.format == "JPEG"


def test_pixel_count_too_large(*, pixel_count_too_large: io.BytesIO) -> None:
    """The image has more pixels than Vuforia allows."""
    with Image.open(fp=pixel_count_too_large) as image:
        assert image.format == "PNG"
        assert image.width * image.height > _MAX_IMAGE_PIXELS
    assert len(pixel_count_too_large.getvalue()) < _MAX_TARGET_IMAGE_BYTES


def test_png_just_under_max_size(
    *,
    png_just_under_max_size: io.BytesIO,
) -> None:
    """The PNG is under the Target API maximum file size."""
    size = len(png_just_under_max_size.getvalue())
    assert size <= _MAX_TARGET_IMAGE_BYTES
    # Stay near the limit so this remains a useful boundary fixture.
    assert size > _MAX_TARGET_IMAGE_BYTES * 0.95
    with Image.open(fp=png_just_under_max_size) as image:
        assert image.format == "PNG"
