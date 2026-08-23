"""``pytest`` fixtures for testing Vuforia Web Services related tools."""

from vws_test_fixtures.images import (
    bad_image_file,
    corrupted_image_file,
    different_high_quality_image,
    high_quality_image,
    image_file_failed_state,
    image_file_success_state_low_rating,
    image_files_failed_state,
    png_too_large,
)

__all__ = [
    "bad_image_file",
    "corrupted_image_file",
    "different_high_quality_image",
    "high_quality_image",
    "image_file_failed_state",
    "image_file_success_state_low_rating",
    "image_files_failed_state",
    "png_too_large",
]
