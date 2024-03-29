Contributing to |project|
=========================

.. contents::
   :local:
   :class: this-will-duplicate-information-and-it-is-still-useful-here

Contributions to this repository must pass tests and linting.

CI is the canonical source of truth.

Install contribution dependencies
---------------------------------

Install Python dependencies in a virtual environment.

.. code:: sh

    pip install --editable '.[dev]'

Spell checking requires ``enchant``.
This can be installed on macOS, for example, with `Homebrew <https://brew.sh>`__:

.. code:: sh

    brew install enchant

and on Ubuntu with ``apt``:

.. code:: sh

    apt-get install -y enchant

Linting
-------

Run lint tools:

.. code:: sh

    make lint

To fix some lint errors, run the following:

.. code:: sh

    make fix-lint

Running tests
-------------

Run ``pytest``:

.. code:: sh

    pytest

Documentation
-------------

Documentation is built on Read the Docs.

Run the following commands to build and view documentation locally:

.. code:: sh

   make docs
   make open-docs

Continuous integration
----------------------

Tests are run on GitHub Actions.
The configuration for this is in :file:`.github/workflows/`.

Performing a release
--------------------

See :doc:`release-process`.
