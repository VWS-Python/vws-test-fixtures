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
    high_quality_image.getvalue()
    image_file_failed_state.getvalue()
    png_too_large.getvalue()
