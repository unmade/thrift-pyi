import copy
from unittest import mock

import pytest

# The right way is to test with different thriftpy2 versions (old one and the one with
# binary support), but I'm too lazy to do it


@pytest.fixture(name="ttype_cls")
def _ttype_cls():
    # pylint: disable=import-outside-toplevel
    from thriftpy2.thrift import TType

    return copy.deepcopy(TType)


@pytest.fixture(name="register_binary")
def _register_binary():
    # pylint: disable=import-outside-toplevel
    from thriftpyi.utils import _register_binary

    return _register_binary


@pytest.fixture(name="normalize_module")
def _normalize_module():
    # pylint: disable=import-outside-toplevel
    from thriftpyi.utils import _normalize_module

    return _normalize_module


@pytest.fixture(name="guess_type")
def _guess_type():
    # pylint: disable=import-outside-toplevel
    from thriftpyi.utils import guess_type

    return guess_type


@pytest.fixture(name="get_module_for_value")
def _get_module_for_value():
    # pylint: disable=import-outside-toplevel
    from thriftpyi.utils import get_module_for_value

    return get_module_for_value


class TestGuessType:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            (1, "int"),
            (1.0, "float"),
            ("string", "str"),
            (True, "bool"),
            ({1, 2}, "Set[int]"),
            ([1, 2], "List[int]"),
            ({"1": "2"}, "Dict[str, str]"),
        ],
    )
    def test(self, guess_type, value, expected: str):
        assert guess_type(value, known_modules=[], known_structs=[]) == expected

    def test_strips_thrift_suffix_from_module(self, guess_type):
        value = mock.Mock()
        value.__class__.__module__ = "foo_thrift_thrift"
        value.__class__.__name__ = "Bar"
        result = guess_type(value, known_modules=["foo_thrift"], known_structs=[])
        assert result == "foo_thrift.Bar"

    def test_resolves_cross_dir_module(self, guess_type):
        value = mock.Mock()
        value.__class__.__module__ = "sub.child_thrift"
        value.__class__.__name__ = "Identifier"
        result = guess_type(
            value,
            known_modules=["child"],
            known_structs=[],
            module_name_map={"sub.child_thrift": "child"},
        )
        assert result == "child.Identifier"


class TestGetModuleForValue:
    def test_strips_thrift_suffix_from_module(self, get_module_for_value):
        value = mock.Mock()
        value.__class__.__module__ = "foo_thrift_thrift"
        result = get_module_for_value(value, known_modules=["foo_thrift"])
        assert result == "foo_thrift"

    def test_resolves_cross_dir_module(self, get_module_for_value):
        value = mock.Mock()
        value.__class__.__module__ = "sub.child_thrift"
        result = get_module_for_value(
            value,
            known_modules=["child"],
            module_name_map={"sub.child_thrift": "child"},
        )
        assert result == "child"


class TestNormalizeModule:
    def test_strips_thrift_suffix(self, normalize_module):
        result = normalize_module("foo_thrift", known_modules=["foo"])
        assert result == "foo"

    def test_cross_dir_include(self, normalize_module):
        result = normalize_module(
            "sub.child_thrift",
            known_modules=["child"],
            module_name_map={"sub.child_thrift": "child"},
        )
        assert result == "child"

    def test_map_takes_precedence(self, normalize_module):
        result = normalize_module(
            "sub.child_thrift",
            known_modules=["sub.child"],
            module_name_map={"sub.child_thrift": "child"},
        )
        assert result == "child"


class TestRegisterBinary:
    def test_when_binary_defined_as_string(self, register_binary, ttype_cls):
        ttype_cls.BINARY = ttype_cls.STRING
        with mock.patch("thriftpy2.thrift.TType", ttype_cls):
            mapping = {}
            register_binary(mapping)
            assert mapping == {}

    def test_when_binary_is_a_standalone_typed(self, register_binary, ttype_cls):
        ttype_cls.BINARY = 18
        with mock.patch("thriftpyi.utils.TType", ttype_cls):
            mapping = {}
            register_binary(mapping)
            assert ttype_cls.BINARY in mapping

    def test_when_ttype_doesnt_define_binary(self, register_binary, ttype_cls):
        del ttype_cls.BINARY
        with mock.patch("thriftpy2.thrift.TType", ttype_cls):
            mapping = {}
            register_binary(mapping)
            assert mapping == {}
