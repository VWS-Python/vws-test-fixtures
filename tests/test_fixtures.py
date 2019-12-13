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
    pass
