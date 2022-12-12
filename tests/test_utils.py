# pylint: disable=import-outside-toplevel

import copy
from unittest import mock

import pytest

# from thriftpyi import TTYPE_BINARY, TTYPE_MAP, _get_binary as get_binary

# The right was is to test with different thriftpy2 versions (old one and the one with
# binary support), but I'm too lazy to do it


def test_register_binary():
    ...


@pytest.fixture(name="ttype_cls")
def _ttype_cls():
    from thriftpy2.thrift import TType

    return copy.deepcopy(TType)


def test_get_binary_returns_str(ttype_cls):
    ttype_cls.BINARY = ttype_cls.STRING
    with mock.patch("thriftpy2.thrift.TType", ttype_cls):
        from thriftpyi.utils import _register_binary

        mapping = {}
        _register_binary(mapping)
        assert mapping == {}


def test_get_binary_returns_bytes(ttype_cls):
    ttype_cls.BINARY = 18
    with mock.patch("thriftpyi.utils.TType", ttype_cls):
        from thriftpyi.utils import _register_binary

        mapping = {}
        _register_binary(mapping)
        assert ttype_cls.BINARY in mapping


def test_get_binary_returns_str_when_ttype_doesnt_define_binary(ttype_cls):
    del ttype_cls.BINARY
    with mock.patch("thriftpy2.thrift.TType", ttype_cls):
        from thriftpyi.utils import _register_binary

        mapping = {}
        _register_binary(mapping)
        assert mapping == {}
