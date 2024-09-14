|project|
=========

``pytest`` fixtures for testing tools with the Vuforia Web Services (VWS) API.

Installation
------------

.. code-block:: shell

   pip install vws-test-fixtures

This is tested on Python 3.12+.

Example usage
-------------

.. code-block:: python

   """Run a test which uses a high quality image."""

   import io


   def test_high_quality_image(high_quality_image: io.BytesIO) -> None:
       """Test that a high quality image is given."""
       image_file_bytes = high_quality_image.getvalue()
       minimum_image_size = 1000
       assert len(image_file_bytes) >= minimum_image_size

All fixtures
------------

Use the names of the following methods as fixture names.

.. automodule:: vws_test_fixtures.images
   :undoc-members:
   :members:

Reference
---------

.. toctree::
   :maxdepth: 3

   contributing
   release-process
   changelog
