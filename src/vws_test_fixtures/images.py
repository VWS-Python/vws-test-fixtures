"""Fixtures for images."""

import io
import secrets
from importlib.resources import files
from typing import Literal

import pytest
from PIL import Image


def _make_image_file(
    file_format: str,
    color_space: Literal["L", "RGB", "CMYK"],
    width: int,
    height: int,
) -> io.BytesIO:
    """An image file in the given format and color space.

    The image file is filled with randomly colored pixels.

    Args:
        file_format: See
            http://pillow.readthedocs.io/en/3.1.x/handbook/image-file-formats.html
        color_space: One of "L", "RGB", or "CMYK".
        width: The width, in pixels of the image.
        height: The width, in pixels of the image.

    Returns:
        An image file in the given format and color space.
    """
    image_buffer = io.BytesIO()
    image = Image.new(mode=color_space, size=(width, height))
    for row_index in range(height):
        for column_index in range(width):
            if color_space == "L":
                grey = secrets.choice(seq=range(255))
                image.putpixel(xy=(column_index, row_index), value=grey)
            else:
                red = secrets.choice(seq=range(255))
                green = secrets.choice(seq=range(255))
                blue = secrets.choice(seq=range(255))
                image.putpixel(
                    xy=(column_index, row_index),
                    value=(red, green, blue),
                )

    image.save(fp=image_buffer, format=file_format)
    image_buffer.seek(0)
    return image_buffer


@pytest.fixture
def high_quality_image() -> io.BytesIO:
    """An image file which is expected to have a 'success' status when
    added to
    a target and a high tracking rating.

    At the time of writing, this image gains a tracking rating of 5.
    """
    resource = files(anchor=__package__) / "high_quality_image.jpg"
    return io.BytesIO(initial_bytes=resource.read_bytes())


@pytest.fixture
def image_file_failed_state() -> io.BytesIO:
    """
    An image file which is expected to be accepted by the add and update
    target
    endpoints, but get a "failed" status.
    """
    # This image gets a "failed" status because it is so small.
    return _make_image_file(
        file_format="PNG",
        color_space="RGB",
        width=1,
        height=1,
    )


@pytest.fixture
def png_too_large() -> io.BytesIO:
    """
    Return a PNG file which has dimensions which are too large to be
    added to a
    Vuforia database.
    """
    width = height = 890

    return _make_image_file(
        file_format="PNG",
        color_space="RGB",
        width=width,
        height=height,
    )


@pytest.fixture
def image_file_success_state_low_rating() -> io.BytesIO:
    """
    An image file which is expected to have a 'success' status when
    added to a
    target and a low rating after processing.
    """
    return _make_image_file(
        file_format="PNG",
        color_space="RGB",
        width=5,
        height=5,
    )


@pytest.fixture
def corrupted_image_file() -> io.BytesIO:
    """An image file which is corrupted."""
    original_image = _make_image_file(
        file_format="PNG",
        color_space="RGB",
        width=1,
        height=1,
    )
    original_data = original_image.getvalue()
    corrupted_data = original_data.replace(b"IEND", b"\x00IEND")
    return io.BytesIO(initial_bytes=corrupted_data)


@pytest.fixture(params=[("PNG", "RGB"), ("JPEG", "RGB"), ("PNG", "L")])
def image_files_failed_state(request: pytest.FixtureRequest) -> io.BytesIO:
    """
    An image file which is expected to be accepted by the add and update
    target
    endpoints, but get a "failed" status.
    """
    # These images get a "failed" status because they are so small.
    file_format, color_space = request.param
    return _make_image_file(
        file_format=file_format,
        color_space=color_space,
        width=1,
        height=1,
    )


@pytest.fixture(
    params=[("TIFF", "RGB"), ("JPEG", "CMYK")],
    ids=["Not accepted format", "Not accepted color space"],
)
def bad_image_file(request: pytest.FixtureRequest) -> io.BytesIO:
    """
    An image file which is expected to cause a `BadImage` result when an
    attempt is made to add it to the target database.
    """
    file_format, color_space = request.param
    return _make_image_file(
        file_format=file_format,
        color_space=color_space,
        width=1,
        height=1,
    )


@pytest.fixture
def different_high_quality_image() -> io.BytesIO:
    """An image file which is expected to have a 'success' status when
    added to
    a target and a high tracking rating.

    This is necessarily different to ``high_quality_image``.
    """
    resource = files(anchor=__package__) / "different_high_quality_image.jpg"
    return io.BytesIO(initial_bytes=resource.read_bytes())


# Vuforia Target API maximum image file size in bytes.
_MAX_TARGET_IMAGE_BYTES = 2_359_293

# Vuforia Query / Cloud Recognition API maximum image file size in bytes.
_MAX_QUERY_IMAGE_BYTES = 2 * 1024 * 1024

# Maximum number of pixels accepted by Vuforia (undocumented; from mock_vws).
_MAX_IMAGE_PIXELS = 37_748_736


def _jpeg_with_minimum_size(*, min_size: int) -> io.BytesIO:
    """Return a valid JPEG whose file size is at least ``min_size`` bytes.

    A minimal JPEG is inflated with COM (comment) markers so the result is
    deterministic and cheap to build, while remaining openable by Pillow.
    """
    image_buffer = io.BytesIO()
    Image.new(mode="RGB", size=(8, 8), color=(255, 0, 0)).save(
        fp=image_buffer,
        format="JPEG",
    )
    jpeg_bytes = image_buffer.getvalue()
    parts = [jpeg_bytes[:2]]  # SOI
    remaining = min_size - len(jpeg_bytes)
    # COM payload length is limited by the 16-bit length field.
    max_payload = 65_533
    while remaining > 0:
        payload_len = min(remaining, max_payload)
        length = payload_len + 2
        com_marker = (
            b"\xff\xfe"
            + length.to_bytes(length=2, byteorder="big")
            + (b"\x00" * payload_len)
        )
        parts.append(com_marker)
        remaining -= payload_len
    parts.append(jpeg_bytes[2:])
    return io.BytesIO(initial_bytes=b"".join(parts))


@pytest.fixture
def jpeg_too_large() -> io.BytesIO:
    """A JPEG larger than the Cloud Recognition 2 MiB query size limit."""
    return _jpeg_with_minimum_size(min_size=_MAX_QUERY_IMAGE_BYTES + 1)


@pytest.fixture
def pixel_count_too_large() -> io.BytesIO:
    """A PNG with more pixels than Vuforia allows, but a small file size.

    Uses a single-color greyscale PNG so compression keeps the file small
    while ``width * height`` exceeds ``_MAX_IMAGE_PIXELS``.

    ``6144 * 6144 == _MAX_IMAGE_PIXELS``; one extra column exceeds the limit.
    """
    width = 6144 + 1
    height = 6144
    image_buffer = io.BytesIO()
    image = Image.new(mode="L", size=(width, height))
    image.save(fp=image_buffer, format="PNG")
    image_buffer.seek(0)
    return image_buffer


@pytest.fixture
def png_just_under_max_size() -> io.BytesIO:
    """A PNG just under the Target API maximum file size (positive
    control).

    With ``compress_level=0``, an 886x886 RGB PNG is a few kibibytes under
    ``_MAX_TARGET_IMAGE_BYTES`` regardless of pixel content.
    """
    width = height = 886
    image_buffer = io.BytesIO()
    image = Image.new(mode="RGB", size=(width, height), color=(1, 2, 3))
    image.save(fp=image_buffer, format="PNG", compress_level=0)
    image_buffer.seek(0)
    return image_buffer
