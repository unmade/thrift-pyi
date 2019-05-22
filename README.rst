========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - | |travis|
        | |requires|
        | |codecov|
        | |codacy|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |travis| image:: https://travis-ci.org/unmade/thrift-pyi.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/unmade/thrift-pyi

.. |requires| image:: https://requires.io/github/unmade/thrift-pyi/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/unmade/thrift-pyi/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/unmade/thrift-pyi/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/unmade/thrift-pyi

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/487480f045594e148309e8b7f1f71351
    :alt: Codacy Badge
    :target: https://app.codacy.com/app/unmade/thrift-pyi

.. |version| image:: https://img.shields.io/pypi/v/thriftpyi.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/thriftpyi

.. |commits-since| image:: https://img.shields.io/github/commits-since/unmade/thrift-pyi/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/unmade/thrift-pyi/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/thriftpyi.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/thriftpyi

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/thriftpyi.svg
    :alt: Supported versions
    :target: https://pypi.org/project/thriftpyi

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/thriftpyi.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/thriftpyi

.. end-badges

This is simple `.pyi` stubs generator from thrift interfaces

* Free software: MIT license

Documentation
=============

Sample usage:

.. code-block:: bash

    $ thriftpyi example/interfaces --output example/app/interfaces

Development
===========

To run the all tests run::

    tox
