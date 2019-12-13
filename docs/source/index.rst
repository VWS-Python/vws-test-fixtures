|project|
=========

``pytest`` fixtures for use when testing tools which interact with Vuforia Web Services.

Installation
------------

.. code:: sh

   pip install vws-test-fixtures

This is tested on Python 3.8+.

Example usage
-------------

.. code:: python

   # A test to be run by pytest
   def test_example(high_quality_image: io.BytesIO) -> None:
       image_file_bytes = high_quality_image.getvalue()
       ...

``high_quality_image`` returns an image file which is expected to have a 'success' status when added to a target, and a high tracking rating.

``image_file_failed_state`` is expected to be accepted by the add and update target endpoints, but get a "failed" status.

``png_too_large`` is a PNG which has dimensions whcih are too large to be added to a Vuforia database.

Reference
---------

.. toctree::
   :maxdepth: 3

   contributing
   release-process
   changelog

