========
Overview
========

.. start-badges

.. image:: https://travis-ci.org/unmade/thrift-pyi.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/unmade/thrift-pyi

.. image:: https://codecov.io/github/unmade/thrift-pyi/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/unmade/thrift-pyi

.. image:: https://api.codacy.com/project/badge/Grade/487480f045594e148309e8b7f1f71351
    :alt: Codacy Badge
    :target: https://app.codacy.com/app/unmade/thrift-pyi

.. image:: https://requires.io/github/unmade/thrift-pyi/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/unmade/thrift-pyi/requirements/?branch=master

.. image:: https://img.shields.io/pypi/v/thriftpyi.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/thriftpyi

.. image:: https://img.shields.io/pypi/wheel/thriftpyi.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/thriftpyi

.. image:: https://img.shields.io/pypi/pyversions/thriftpyi.svg
    :alt: Supported versions
    :target: https://pypi.org/project/thriftpyi

.. image:: https://img.shields.io/badge/License-MIT-purple.svg
    :alt: MIT License
    :target: https://github.com/unmade/thrift-pyi/blob/master/LICENSE

.. end-badges

This is simple `.pyi` stubs generator from thrift interfaces.
Motivation for this project was to have autocomplete and type checking
for dynamically loaded thrift interfaces

Installation
============

.. code-block:: bash

    pip install thriftpyi

Quickstart
=============

Sample usage:

.. code-block:: bash

    $ thriftpyi example/interfaces --output example/app/interfaces

Additionally to generated stubs it is required to create `__init__.py` that will load thrift interfaces, for example:

.. code-block:: python

    from pathlib import Path
    from types import ModuleType
    from typing import Dict

    import thriftpy2

    _interfaces_path = Path("example/interfaces")
    _interfaces: Dict[str, ModuleType] = {}


    def __getattr__(name):
        try:
            return _interfaces[name]
        except KeyError:
            _interfaces[name] = thriftpy2.load(
                str(_interfaces_path.joinpath(f"{name}.thrift"))
            )
            return _interfaces[name]

To see more detailed example of usage refer to `example app <https://github.com/unmade/thrift-pyi/blob/master/example>`_

Development
===========

To run the all tests run::

    tox
