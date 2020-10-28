from unittest import mock

from thriftpyi.utils import _get_binary as get_binary

# This should be redo with 'skipif' and different
# thriftpy2 versions (old one and the one with binary support)


def test_get_binary_returns_str():
    with mock.patch("thriftpy2.thrift.TType.BINARY", 11):
        assert get_binary([]) == "str"


def test_get_binary_returns_bytes():
    with mock.patch("thriftpy2.thrift.TType.BINARY", 18):
        assert get_binary([]) == "bytes"
