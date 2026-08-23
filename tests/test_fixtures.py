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
    exif_oriented_jpeg: io.BytesIO,
    animated_gif: io.BytesIO,
    webp_image: io.BytesIO,
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
        exif_oriented_jpeg.getvalue(),
        animated_gif.getvalue(),
        webp_image.getvalue(),
    ]
    assert len(set(fixture_bytes_list)) == len(fixture_bytes_list)


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
        assert getattr(image, "is_animated", False)
        n_frames = getattr(image, "n_frames", 1)
        assert n_frames > 1


def test_webp_image(*, webp_image: io.BytesIO) -> None:
    """The WebP fixture is a valid WebP image."""
    with Image.open(fp=webp_image) as image:
        assert image.format == "WEBP"
