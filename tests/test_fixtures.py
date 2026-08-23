"""Test for the new fixtures."""

import base64
import io
from pathlib import Path

import pytest
from PIL import Image, UnidentifiedImageError

import vws_test_fixtures
from vws_test_fixtures.images import VWS_MAX_IMAGE_FILE_SIZE

_MIN_HIGH_QUALITY_DIMENSION = 100
_PNG_TOO_LARGE_DIMENSION = 900
_MAX_QUERY_IMAGE_BYTES = 2 * 1024 * 1024
_MAX_IMAGE_PIXELS = 37_748_736
_MAX_METADATA_BYTES = 1024 * 1024 - 1


def test_image_fixtures(  # pylint: disable=too-many-locals
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
    exif_oriented_jpeg: io.BytesIO,
    animated_gif: io.BytesIO,
    webp_image: io.BytesIO,
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
        empty_file.getvalue(),
        grayscale_jpeg.getvalue(),
        rgba_png.getvalue(),
        exif_oriented_jpeg.getvalue(),
        animated_gif.getvalue(),
        webp_image.getvalue(),
        jpeg_too_large.getvalue(),
        pixel_count_too_large.getvalue(),
        png_just_under_max_size.getvalue(),
    ]
    assert len(set(fixture_bytes_list)) == len(fixture_bytes_list)


def test_png_too_large_exceeds_vws_file_size_limit(
    png_too_large: io.BytesIO,
) -> None:
    """``png_too_large`` exceeds the VWS image file size limit."""
    assert len(png_too_large.getvalue()) > VWS_MAX_IMAGE_FILE_SIZE


def test_corrupted_image_file_not_openable_by_pillow(
    *,
    corrupted_image_file: io.BytesIO,
) -> None:
    """``corrupted_image_file`` cannot be opened by Pillow."""
    with pytest.raises(expected_exception=UnidentifiedImageError):
        Image.open(fp=corrupted_image_file)


def test_image_fixture_buffer_starts_at_beginning(
    *,
    high_quality_image: io.BytesIO,
) -> None:
    """Fixture buffers are readable from position ``0``; ``getvalue`` still
    works.
    """
    assert high_quality_image.tell() == 0
    contents = high_quality_image.read()
    assert contents
    assert high_quality_image.tell() == len(contents)
    assert high_quality_image.getvalue() == contents


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
        transparent_pixel = image.getpixel(xy=(1, 1))
        opaque_pixel = image.getpixel(xy=(0, 0))
        assert isinstance(transparent_pixel, tuple)
        assert isinstance(opaque_pixel, tuple)
        assert transparent_pixel[3] == 0
        assert opaque_pixel[3] == opaque_alpha


def test_exif_oriented_jpeg(*, exif_oriented_jpeg: io.BytesIO) -> None:
    """The EXIF-oriented JPEG has Orientation set to 6."""
    orientation_tag = 0x0112
    expected_orientation = 6
    with Image.open(fp=exif_oriented_jpeg) as image:
        assert image.format == "JPEG"
        assert image.getexif()[orientation_tag] == expected_orientation


def test_animated_gif(*, animated_gif: io.BytesIO) -> None:
    """The animated GIF fixture has more than one frame."""
    with Image.open(fp=animated_gif) as image:
        assert image.format == "GIF"
        assert image.is_animated
        assert image.n_frames > 1


def test_webp_image(*, webp_image: io.BytesIO) -> None:
    """The WebP fixture is a valid WebP image."""
    with Image.open(fp=webp_image) as image:
        assert image.format == "WEBP"


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
    assert len(pixel_count_too_large.getvalue()) < VWS_MAX_IMAGE_FILE_SIZE


def test_png_just_under_max_size(
    *,
    png_just_under_max_size: io.BytesIO,
) -> None:
    """The PNG is under the Target API maximum file size."""
    size = len(png_just_under_max_size.getvalue())
    assert size <= VWS_MAX_IMAGE_FILE_SIZE
    # Stay near the limit so this remains a useful boundary fixture.
    assert size > VWS_MAX_IMAGE_FILE_SIZE * 0.95
    with Image.open(fp=png_just_under_max_size) as image:
        assert image.format == "PNG"


def test_application_metadata_near_size_limit(
    *,
    application_metadata_near_size_limit: str,
) -> None:
    """Metadata decodes to the maximum allowed number of bytes."""
    decoded = base64.b64decode(
        s=application_metadata_near_size_limit.encode(encoding="ascii"),
    )
    assert len(decoded) == _MAX_METADATA_BYTES


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


def test_package_reexports_image_fixtures() -> None:
    """Image fixtures are importable from the package root."""
    assert vws_test_fixtures.high_quality_image is not None
    assert "high_quality_image" in vws_test_fixtures.__all__
