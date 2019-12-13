"""
Test for the new fixtures.
"""

import io

pytest_plugins = 'pytester'  # pylint: disable=invalid-name


def test_example(
    high_quality_image: io.BytesIO,
    image_file_failed_state: io.BytesIO,
    png_too_large: io.BytesIO,
) -> None:
    """
    The image functions can be used as fixtures.
    """
    high_quality_image_bytes = high_quality_image.getvalue()
    image_failed_state_bytes = image_file_failed_state.getvalue()
    png_too_large_bytes = png_too_large.getvalue()
    fixture_bytes = [
        high_quality_image_bytes,
        image_failed_state_bytes,
        png_too_large_bytes,
    ]
    assert len(set(fixture_bytes)) == 3
