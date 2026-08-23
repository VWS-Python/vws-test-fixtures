Changelog
=========

.. contents::
   :local:
   :class: this-will-duplicate-information-and-it-is-still-useful-here

.. towncrier release notes start

2026.08.23
----------

- Fill image fixtures with fast, deterministic pixel data and ensure ``png_too_large`` exceeds the VWS size limit

- Fix the ``_make_image_file`` docstring to document ``height`` as height, not width

- Fill CMYK image fixtures with CMYK 4-tuples instead of RGB triplets

- Include pixel value ``255`` when filling random image fixtures

- Add a ``jpeg_too_large`` fixture exceeding the Cloud Recognition 2 MiB limit.

- Add a ``pixel_count_too_large`` fixture exceeding Vuforia's pixel limit.

- - Truncate ``corrupted_image_file`` so Pillow cannot open or repair it.

- - Use BMP instead of TIFF for the unsupported ``bad_image_file`` format.

- - Add a greyscale JPEG variant to ``image_files_failed_state``.

- - Share failed-state image params between the single and parametrized fixtures.

- Add an ``empty_file`` fixture returning a zero-byte ``BytesIO``.

- Add a ``grayscale_jpeg`` fixture returning a valid greyscale JPEG.

- Add an ``rgba_png`` fixture returning an RGBA PNG with transparency.

- - Clarify that ``high_quality_image``'s historical rating of 5 is observational, not guaranteed.

- - Document that bundled high-quality JPEGs are not re-scored against live Vuforia in CI.

- - Assert the two high-quality image fixtures differ as pixel arrays, not only as bytes.

- - Return a fresh ``BytesIO`` from cached image bytes on each fixture call.

- - Cache expensive generated image bytes so they are not rebuilt every test.

- - Assert fixture images have the expected Pillow format, mode, and dimensions.

- - Add a test that ``corrupted_image_file`` raises when opened with Pillow.

- Pass PNG and JPEG optimization flags when saving generated image fixtures

- - Fill CMYK fixtures with four-channel pixels so JPEG+CMYK saves correctly.

- Add pytest ids to ``image_files_failed_state`` params for clearer failure names

- Add a ``png_just_under_max_size`` boundary-good Target API size fixture.

- Add an ``exif_oriented_jpeg`` fixture with EXIF Orientation set.

- Add an ``animated_gif`` multi-frame GIF fixture.

- Add a ``webp_image`` fixture returning a valid WebP image.

- Branch ``_make_image_file`` pixel filling on ``color_space`` so CMYK and RGB paths are distinct

- - Re-export image fixtures from the package root with an explicit ``__all__``.

- - Document typed fixture exports. The package already includes ``py.typed``.

- - Cache packaged JPEG resource bytes instead of reloading on every fixture call.

- - Document that ``image_file_success_state_low_rating`` does not guarantee a low Vuforia rating.

- - Add ``Path`` fixtures that write high-quality images to temporary files.

- Add ``ClearNamespaceParser`` to the root Sybil ``conftest`` setup.

- Add ``application_metadata_near_size_limit`` base64 metadata fixture.

2026.08.16
----------

No documented changes.

2023.03.05
------------

2022.01.03
------------

2021.11.05.1
------------

2021.11.05.0
------------
