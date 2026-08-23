"""Test for the new fixtures."""

import io

from PIL import Image


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
    empty_file: io.BytesIO,
    grayscale_jpeg: io.BytesIO,
    rgba_png: io.BytesIO,
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
        empty_file.getvalue(),
        grayscale_jpeg.getvalue(),
        rgba_png.getvalue(),
    ]
    assert len(set(fixture_bytes_list)) == len(fixture_bytes_list)


def test_empty_file(*, empty_file: io.BytesIO) -> None:
    """The empty file fixture has no bytes."""
    assert empty_file.getvalue() == b""


def test_grayscale_jpeg(*, grayscale_jpeg: io.BytesIO) -> None:
    """The greyscale JPEG fixture is a mode-L JPEG."""
    with Image.open(fp=grayscale_jpeg) as image:
        assert image.format == "JPEG"
        assert image.mode == "L"


def test_rgba_png(*, rgba_png: io.BytesIO) -> None:
    """The RGBA PNG fixture has transparency."""
    opaque_alpha = 255
    with Image.open(fp=rgba_png) as image:
        assert image.format == "PNG"
        assert image.mode == "RGBA"
        assert image.getpixel(xy=(1, 1))[3] == 0
        assert image.getpixel(xy=(0, 0))[3] == opaque_alpha
