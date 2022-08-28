========
Overview
========

.. start-badges

.. image:: https://github.com/unmade/thrift-pyi/workflows/lint%20and%20test/badge.svg?branch=master
    :alt: Build Status
    :target: https://github.com/unmade/thrift-pyi/blob/master/.github/workflows/lint-and-test.yml

.. image:: https://codecov.io/github/unmade/thrift-pyi/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/unmade/thrift-pyi

.. image:: https://api.codacy.com/project/badge/Grade/487480f045594e148309e8b7f1f71351
    :alt: Codacy Badge
    :target: https://app.codacy.com/app/unmade/thrift-pyi

.. image:: https://requires.io/github/unmade/thrift-pyi/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/unmade/thrift-pyi/requirements/?branch=master

.. image:: https://img.shields.io/pypi/v/thrift-pyi.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/thrift-pyi

.. image:: https://img.shields.io/pypi/wheel/thrift-pyi.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/thrift-pyi

.. image:: https://img.shields.io/pypi/pyversions/thrift-pyi.svg
    :alt: Supported versions
    :target: https://pypi.org/project/thrift-pyi

.. image:: https://img.shields.io/badge/License-MIT-purple.svg
    :alt: MIT License
    :target: https://github.com/unmade/thrift-pyi/blob/master/LICENSE

.. end-badges

This is simple `.pyi` stubs generator from thrift interfaces.
Motivation for this project is to have autocomplete and type checking
for dynamically loaded thrift interfaces

Installation
============

.. code-block:: bash

    pip install thrift-pyi

Quickstart
==========

Sample usage:

.. code-block:: bash

    $ thriftpyi example/interfaces --output example/app/interfaces

Additionally to generated stubs you might want to create `__init__.py` that will load thrift interfaces, for example:

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
            interface = thriftpy2.load(str(_interfaces_path.joinpath(f"{name}.thrift")))
            _interfaces[name] = interface
            return interface


To see more detailed example of usage refer to `example app <https://github.com/unmade/thrift-pyi/blob/master/example>`_

--strict-optional
-----------------

Python and thrift are very different at argument handling.
For example in thrift the following will be correct declaration:

.. code-block:: thrift

    struct TodoItem {
        1: required i32 id
        3: optional i32 type = 1
        2: required string text
    }

In python, fields without default values cannot appear after fields with default
values. Therefore by default all fields are optional with default to None.
This is compliant to `thriftpy2 <https://github.com/Thriftpy/thriftpy2>`_.

However, if you want more strict behaviour you can specify `--strict-optional` option.
For the case above, the following stubs will be generated:

.. code-block:: python

    from dataclasses import dataclass

    @dataclass
    class TodoItem:
        id: int
        type: int = 1
        text: str

Development
===========

To install pre-commit hooks::

    pre-commit install

To run the all tests run::

    tox
