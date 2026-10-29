VWS Test Fixtures
=================

This package's Cloud Image Recognition fixtures have been removed.
PTC has announced that Vuforia Engine Cloud Image Recognition and its cloud image databases retire on May 2, 2027.

The package no longer exports fixtures or registers a pytest plugin, and it has no runtime dependencies.
Remove ``vws-test-fixtures`` from projects that now use only Model Targets or VuMarks.
Legacy cloud image tests require an earlier release.

.. code-block:: python

   """Import the retired package without registering cloud fixtures."""

   import vws_test_fixtures

   assert vws_test_fixtures.__all__ == []

See the `historical release notes <https://vws-python.github.io/vws-test-fixtures/changelog.html>`_ for earlier fixtures.
