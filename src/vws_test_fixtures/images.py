"""Fixtures for images."""

import io
import secrets
from pathlib import Path
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
    path = Path(__file__).parent / "high_quality_image.jpg"
    return io.BytesIO(initial_bytes=path.read_bytes())


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
    path = Path(__file__).parent / "different_high_quality_image.jpg"
    return io.BytesIO(initial_bytes=path.read_bytes())
