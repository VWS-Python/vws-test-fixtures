|project|
=========

``pytest`` fixtures for testing tools with the Vuforia Web Services (VWS) API.

Installation
------------

.. code:: sh

   pip install vws-test-fixtures

This is tested on Python 3.12+.

Example usage
-------------

.. code:: python

   import io

   # A test to be run by pytest
   def test_example(high_quality_image: io.BytesIO) -> None:
       image_file_bytes = high_quality_image.getvalue()
       ...

.. -> test_src

.. invisible-code-block: python

   import pathlib
   import subprocess
   import tempfile

   import pytest

   with tempfile.TemporaryDirectory() as tmp_dir:
       test_file = pathlib.Path(tmp_dir) / 'test_src.py'
       test_file.write_text(test_src)
       subprocess.check_output(["python", "-m", "pytest", test_file, "--basetemp", test_file.parent])

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

