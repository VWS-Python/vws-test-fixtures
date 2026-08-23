"""Test for the new fixtures."""

import io

from PIL import Image

_MIN_HIGH_QUALITY_DIMENSION = 100
_PNG_TOO_LARGE_DIMENSION = 890


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


def test_high_quality_image_format(
    *,
    high_quality_image: io.BytesIO,
) -> None:
    """``high_quality_image`` is a JPEG RGB image with non-trivial
    size.
    """
    with Image.open(fp=high_quality_image) as image:
        assert image.format == "JPEG"
        assert image.mode == "RGB"
        width, height = image.size
        assert width >= _MIN_HIGH_QUALITY_DIMENSION
        assert height >= _MIN_HIGH_QUALITY_DIMENSION


def test_different_high_quality_image_format(
    *,
    different_high_quality_image: io.BytesIO,
) -> None:
    """``different_high_quality_image`` is a JPEG RGB image with non-
    trivial
    size.
    """
    with Image.open(fp=different_high_quality_image) as image:
        assert image.format == "JPEG"
        assert image.mode == "RGB"
        width, height = image.size
        assert width >= _MIN_HIGH_QUALITY_DIMENSION
        assert height >= _MIN_HIGH_QUALITY_DIMENSION


def test_high_quality_images_are_visually_distinct(
    *,
    high_quality_image: io.BytesIO,
    different_high_quality_image: io.BytesIO,
) -> None:
    """The two high-quality fixtures are not the same pixel array."""
    with (
        Image.open(fp=high_quality_image) as first,
        Image.open(fp=different_high_quality_image) as second,
    ):
        assert first.get_flattened_data() != second.get_flattened_data()


def test_image_file_failed_state_format(
    *,
    image_file_failed_state: io.BytesIO,
) -> None:
    """``image_file_failed_state`` is a 1x1 RGB PNG."""
    with Image.open(fp=image_file_failed_state) as image:
        assert image.format == "PNG"
        assert image.mode == "RGB"
        assert image.size == (1, 1)


def test_png_too_large_format(*, png_too_large: io.BytesIO) -> None:
    """``png_too_large`` is an RGB PNG larger than Vuforia accepts."""
    with Image.open(fp=png_too_large) as image:
        assert image.format == "PNG"
        assert image.mode == "RGB"
        width, height = image.size
        assert width == _PNG_TOO_LARGE_DIMENSION
        assert height == _PNG_TOO_LARGE_DIMENSION


def test_image_file_success_state_low_rating_format(
    *,
    image_file_success_state_low_rating: io.BytesIO,
) -> None:
    """``image_file_success_state_low_rating`` is a 5x5 RGB PNG."""
    with Image.open(fp=image_file_success_state_low_rating) as image:
        assert image.format == "PNG"
        assert image.mode == "RGB"
        assert image.size == (5, 5)
