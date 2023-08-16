from collections.abc import Collection, Mapping
from typing import List, Tuple

from thriftpy2.thrift import TType


def guess_type(value) -> str:
    if isinstance(value, (bool, int, float, str, bytes)):
        return type(value).__name__
    if isinstance(value, Mapping):
        type_ = type(value).__name__.capitalize()
        key_type = guess_type(list(value.keys())[0])
        value_type = guess_type(list(value.values())[0])
        return f"{type_}[{key_type}, {value_type}]"
    if isinstance(value, Collection):
        type_ = type(value).__name__.capitalize()
        item_type = guess_type(next(iter(value)))
        return f"{type_}[{item_type}]"
    return "Any"


def get_python_type(ttype: int, meta: List) -> str:
    return TTYPE_MAP[ttype](meta)


def _get_bool(meta: List) -> str:
    del meta
    return "bool"


def _get_double(meta: List) -> str:
    del meta
    return "float"


def _get_byte(meta: List) -> str:
    del meta
    return "int"


def _get_binary(meta: List) -> str:
    del meta
    return "bytes"


def _get_i16(meta: List) -> str:
    del meta
    return "int"


def _get_i32(meta: List) -> str:
    del meta
    return "int"


def _get_i64(meta: List) -> str:
    del meta
    return "int"


def _get_str(meta: List) -> str:
    del meta
    return "str"


def _get_struct(meta: List) -> str:
    return f"{meta[0].__module__}.{meta[0].__name__}"


def _get_list(meta: List) -> str:
    subttype, submeta = _unpack_meta(meta)
    return f"List[{get_python_type(subttype, submeta)}]"


def _get_map(meta: List) -> str:
    key, value = meta[0]
    key_ttype, key_meta = _unpack_meta([key])
    value_ttype, value_meta = _unpack_meta([value])
    key_pytype = get_python_type(key_ttype, key_meta)
    value_pytype = get_python_type(value_ttype, value_meta)
    return f"Dict[{key_pytype}, {value_pytype}]"


def _get_set(meta: List) -> str:
    subttype, submeta = _unpack_meta(meta)
    return f"Set[{get_python_type(subttype, submeta)}]"


def _unpack_meta(meta: List) -> Tuple[int, List]:
    try:
        subttype, submeta = meta[0]
    except TypeError:
        subttype, submeta = meta[0], None
    return subttype, [submeta]


def _register_binary(mapping):
    ttype_binary = getattr(TType, "BINARY", TType.STRING)
    if ttype_binary != TType.STRING:
        mapping[ttype_binary] = _get_binary


TTYPE_MAP = {
    TType.BOOL: _get_bool,
    TType.DOUBLE: _get_double,
    TType.BYTE: _get_byte,
    TType.I16: _get_i16,
    TType.I32: _get_i32,
    TType.I64: _get_i64,
    TType.STRING: _get_str,
    TType.STRUCT: _get_struct,
    TType.MAP: _get_map,
    TType.SET: _get_set,
    TType.LIST: _get_list,
}


_register_binary(TTYPE_MAP)
