|project|
=========

``pytest`` fixtures for testing tools with the Vuforia Web Services (VWS) API.

Installation
------------

.. code:: sh

   pip install vws-test-fixtures

This is tested on Python 3.11+.

Example usage
-------------

.. code:: python

   # A test to be run by pytest
   def test_example(high_quality_image: io.BytesIO) -> None:
       image_file_bytes = high_quality_image.getvalue()
       ...

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

