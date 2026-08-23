"""Fixtures for images."""

import io
import random
from importlib.resources import files
from typing import Literal

import pytest
from PIL import Image

_COLOR_SPACE_BANDS = {
    "L": 1,
    "RGB": 3,
    "CMYK": 4,
}

# Vuforia Web Services rejects images larger than 2_359_293 bytes.
VWS_MAX_IMAGE_FILE_SIZE = 2_359_293


def _make_image_file(
    file_format: str,
    color_space: Literal["L", "RGB", "CMYK"],
    width: int,
    height: int,
    *,
    seed: int,
) -> io.BytesIO:
    """An image file in the given format and color space.

    The image file is filled with deterministic pseudo-random pixels.

    Args:
        file_format: See
            http://pillow.readthedocs.io/en/3.1.x/handbook/image-file-formats.html
        color_space: One of "L", "RGB", or "CMYK".
        width: The width, in pixels of the image.
        height: The width, in pixels of the image.
        seed: Seed for pixel data so fixture bytes are reproducible.

    Returns:
        An image file in the given format and color space.
    """
    bands = _COLOR_SPACE_BANDS[color_space]
    # Deterministic fixture data, not cryptography.
    rng = random.Random(x=seed)  # noqa: S311
    pixel_data = rng.randbytes(n=width * height * bands)
    image = Image.frombytes(
        mode=color_space,
        size=(width, height),
        data=pixel_data,
    )
    image_buffer = io.BytesIO()
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
        seed=0,
    )


@pytest.fixture
def png_too_large() -> io.BytesIO:
    """
    Return a PNG file which has dimensions which are too large to be
    added to a
    Vuforia database.
    """
    # Vuforia Web Services rejects images larger than 2_359_293 bytes.
    # 900x900 RGB noise reliably exceeds ``VWS_MAX_IMAGE_FILE_SIZE``.
    width = height = 900

    return _make_image_file(
        file_format="PNG",
        color_space="RGB",
        width=width,
        height=height,
        seed=0,
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
        seed=0,
    )


@pytest.fixture
def corrupted_image_file() -> io.BytesIO:
    """An image file which is corrupted."""
    original_image = _make_image_file(
        file_format="PNG",
        color_space="RGB",
        width=1,
        height=1,
        seed=1,
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
        seed=2,
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
        seed=3,
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
