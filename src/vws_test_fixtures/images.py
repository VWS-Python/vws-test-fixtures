"""Fixtures for images."""

import io
import random
from functools import cache
from importlib.resources import files
from pathlib import Path
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

# Vuforia Query / Cloud Recognition API maximum image file size in bytes.
_MAX_QUERY_IMAGE_BYTES = 2 * 1024 * 1024

# Maximum number of pixels accepted by Vuforia (undocumented; from mock_vws).
_MAX_IMAGE_PIXELS = 37_748_736

_FAILED_STATE_IMAGE_PARAMS: tuple[
    tuple[Literal["PNG", "JPEG"], Literal["L", "RGB"]],
    ...,
] = (
    ("PNG", "RGB"),
    ("JPEG", "RGB"),
    ("PNG", "L"),
    ("JPEG", "L"),
)


def _bytes_io(data: bytes) -> io.BytesIO:
    """Return a fresh ``BytesIO`` wrapping ``data``.

    Each call returns an independent buffer at position ``0``, so consumers
    that ``read()`` without seeking do not affect later fixture uses.
    """
    return io.BytesIO(initial_bytes=data)


@cache
def _load_resource_bytes(name: str) -> bytes:
    """Load packaged image resource bytes once per process."""
    resource = files(anchor=__package__) / name
    return resource.read_bytes()


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
        height: The height, in pixels of the image.
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
    if file_format == "PNG":
        image.save(fp=image_buffer, format=file_format, optimize=True)
    elif file_format == "JPEG":
        image.save(
            fp=image_buffer,
            format=file_format,
            quality=95,
            optimize=True,
        )
    else:
        image.save(fp=image_buffer, format=file_format)
    return _bytes_io(data=image_buffer.getvalue())


@cache
def _png_too_large_bytes() -> bytes:
    """Generate the oversized PNG once per process."""
    # 900x900 RGB noise reliably exceeds ``VWS_MAX_IMAGE_FILE_SIZE``.
    width = height = 900
    return _make_image_file(
        file_format="PNG",
        color_space="RGB",
        width=width,
        height=height,
        seed=0,
    ).getvalue()


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
    return _bytes_io(data=b"".join(parts))


@pytest.fixture
def high_quality_image() -> io.BytesIO:
    """An image file which is expected to have a 'success' status when
    added to
    a target and a high tracking rating.

    Historically this image has received a tracking rating of 5 from
    Vuforia. That observation is not a runtime guarantee: Vuforia's
    rating thresholds can change, and this fixture does not contact
    Vuforia or assert a minimum rating.

    That rating is not checked in this package's CI: Vuforia's scoring
    can change. Re-check against a real database when bumping the
    bundled JPEG.
    """
    return _bytes_io(
        data=_load_resource_bytes(name="high_quality_image.jpg"),
    )


@pytest.fixture
def image_file_failed_state() -> io.BytesIO:
    """
    An image file which is expected to be accepted by the add and update
    target
    endpoints, but get a "failed" status.
    """
    # This image gets a "failed" status because it is so small.
    file_format, color_space = _FAILED_STATE_IMAGE_PARAMS[0]
    return _make_image_file(
        file_format=file_format,
        color_space=color_space,
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
    return _bytes_io(data=_png_too_large_bytes())


@pytest.fixture
def image_file_success_state_low_rating() -> io.BytesIO:
    """
    An image file which is expected to have a 'success' status when
    added to a
    target and a low rating after processing.

    The image is a small random PNG. A low tracking rating is typical
    but not guaranteed: Vuforia ratings are nondeterministic and can
    vary across accounts, regions, and time. This fixture does not
    contact Vuforia or assert a rating.
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
    """An image file which is corrupted.

    The file keeps the PNG signature and the header chunk, and drops every
    chunk after them, so Pillow cannot open it.

    Keeping the signature alone is not suitable.  Vuforia Web Services
    answers such a file with a ``500`` response and a ``Fail`` result code,
    where it answers every other malformed image with ``BadImage``.
    Replacing chunk markers (for example ``IEND``) is not reliable either:
    Pillow may still decode the remaining bytes.
    """
    original_image = _make_image_file(
        file_format="PNG",
        color_space="RGB",
        width=1,
        height=1,
        seed=1,
    )
    original_data = original_image.getvalue()
    png_signature_length = 8
    # The header chunk is a 4 byte length, a 4 byte type, 13 bytes of data,
    # and a 4 byte checksum.
    png_header_chunk_length = 25
    header_length = png_signature_length + png_header_chunk_length
    corrupted_data = original_data[:header_length]
    return _bytes_io(data=corrupted_data)


@pytest.fixture(
    params=_FAILED_STATE_IMAGE_PARAMS,
    ids=["PNG-RGB", "JPEG-RGB", "PNG-L", "JPEG-L"],
)
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
    params=[("BMP", "RGB"), ("JPEG", "CMYK")],
    ids=["Not accepted format", "Not accepted color space"],
)
def bad_image_file(request: pytest.FixtureRequest) -> io.BytesIO:
    """
    An image file which is expected to cause a `BadImage` result when an
    attempt is made to add it to the target database.

    VWS accepts PNG and JPEG in RGB or greyscale.  BMP is used for the
    unsupported-format case because Pillow writes it reliably across
    platforms, unlike TIFF.
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
    Like ``high_quality_image``, the tracking rating is not verified in
    CI against live Vuforia thresholds.
    """
    return _bytes_io(
        data=_load_resource_bytes(name="different_high_quality_image.jpg"),
    )


@pytest.fixture
def high_quality_image_path(  # pylint: disable=redefined-outer-name
    high_quality_image: io.BytesIO,
    tmp_path: Path,
) -> Path:
    """Write ``high_quality_image`` to a temporary file and return its
    path.

    Useful for CLI and other APIs that require a filesystem path.
    """
    image_path = tmp_path / "high_quality_image.jpg"
    image_path.write_bytes(data=high_quality_image.getvalue())
    return image_path


@pytest.fixture
def different_high_quality_image_path(  # pylint: disable=redefined-outer-name
    different_high_quality_image: io.BytesIO,
    tmp_path: Path,
) -> Path:
    """Write ``different_high_quality_image`` bytes to a temporary path.

    Useful for CLI and other APIs that require a filesystem path.
    """
    image_path = tmp_path / "different_high_quality_image.jpg"
    image_path.write_bytes(data=different_high_quality_image.getvalue())
    return image_path


@pytest.fixture
def empty_file() -> io.BytesIO:
    """An empty (zero-byte) file."""
    return io.BytesIO()


@pytest.fixture
def grayscale_jpeg() -> io.BytesIO:
    """A valid greyscale (mode ``L``) JPEG image file."""
    return _make_image_file(
        file_format="JPEG",
        color_space="L",
        width=1,
        height=1,
        seed=4,
    )


@pytest.fixture
def rgba_png() -> io.BytesIO:
    """A PNG image in RGBA mode with some transparent pixels."""
    image_buffer = io.BytesIO()
    image = Image.new(mode="RGBA", size=(2, 2), color=(255, 0, 0, 0))
    image.putpixel(xy=(0, 0), value=(0, 255, 0, 255))
    image.save(fp=image_buffer, format="PNG")
    return _bytes_io(data=image_buffer.getvalue())


@pytest.fixture
def exif_oriented_jpeg() -> io.BytesIO:
    """A JPEG with an EXIF Orientation tag set (Orientation=6)."""
    image_buffer = io.BytesIO()
    image = Image.new(mode="RGB", size=(2, 3), color=(255, 0, 0))
    exif = Image.Exif()
    # EXIF Orientation tag; 6 means rotated 90 degrees CW.
    orientation_tag = 0x0112
    rotate_90_cw = 6
    exif[orientation_tag] = rotate_90_cw
    image.save(fp=image_buffer, format="JPEG", exif=exif)
    return _bytes_io(data=image_buffer.getvalue())


@pytest.fixture
def animated_gif() -> io.BytesIO:
    """A multi-frame animated GIF, which Vuforia rejects."""
    image_buffer = io.BytesIO()
    frame_one = Image.new(mode="RGB", size=(1, 1), color=(255, 0, 0))
    frame_two = Image.new(mode="RGB", size=(1, 1), color=(0, 0, 255))
    frame_one.save(
        fp=image_buffer,
        format="GIF",
        save_all=True,
        append_images=[frame_two],
        duration=100,
        loop=0,
    )
    return _bytes_io(data=image_buffer.getvalue())


@pytest.fixture
def webp_image() -> io.BytesIO:
    """A valid WebP image file."""
    image_buffer = io.BytesIO()
    image = Image.new(mode="RGB", size=(1, 1), color=(0, 128, 255))
    image.save(fp=image_buffer, format="WEBP")
    return _bytes_io(data=image_buffer.getvalue())


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
    return _bytes_io(data=image_buffer.getvalue())


@pytest.fixture
def png_just_under_max_size() -> io.BytesIO:
    """A PNG just under the Target API maximum file size (positive
    control).

    With ``compress_level=0``, an 886x886 RGB PNG is a few kibibytes under
    ``VWS_MAX_IMAGE_FILE_SIZE`` regardless of pixel content.
    """
    width = height = 886
    image_buffer = io.BytesIO()
    image = Image.new(mode="RGB", size=(width, height), color=(1, 2, 3))
    image.save(fp=image_buffer, format="PNG", compress_level=0)
    return _bytes_io(data=image_buffer.getvalue())
