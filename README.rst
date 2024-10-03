|Build Status| |codecov| |PyPI| |Documentation Status|

VWS Test Fixtures
==================

``pytest`` fixtures for testing tools with the Vuforia Web Services (VWS) API.

Installation
------------

.. code-block:: shell

   pip install vws-test-fixtures

This is tested on Python |minimum-python-version|\+.

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

``high_quality_image`` returns an image file which is expected to have a 'success' status when added to a target, and a high tracking rating.

``image_file_failed_state`` is expected to be accepted by the add and update target endpoints, but get a "failed" status.

``png_too_large`` is a PNG which has dimensions whcih are too large to be added to a Vuforia database.

... and more, see the `full documentation <https://vws-test-fixtures.readthedocs.io/en/latest>`__ for details of all fixtures provided.

Full Documentation
------------------

See the `full documentation <https://vws-test-fixtures.readthedocs.io/en/latest>`__.

.. |Build Status| image:: https://github.com/VWS-Python/vws-test-fixtures/actions/workflows/ci.yml/badge.svg?branch=main
   :target: https://github.com/VWS-Python/vws-test-fixtures/actions
.. |codecov| image:: https://codecov.io/gh/VWS-Python/vws-test-fixtures/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/VWS-Python/vws-test-fixtures
.. |Documentation Status| image:: https://readthedocs.org/projects/vws-test-fixtures/badge/?version=latest
   :target: https://vws-test-fixtures.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. |PyPI| image:: https://badge.fury.io/py/VWS-Test-Fixtures.svg
   :target: https://badge.fury.io/py/VWS-Test-Fixtures
.. |minimum-python-version| replace:: 3.12
