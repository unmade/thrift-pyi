from __future__ import annotations

import functools
from collections.abc import Collection, Mapping
from typing import Any

from thriftpy2.thrift import TType


def guess_type(  # pylint: disable=too-many-branches
    value,
    *,
    module_name_map: dict[str, str],
    known_structs: Collection[type[Any]],
) -> str:
    if isinstance(value, (bool, int, float, str, bytes)):
        return type(value).__name__

    if isinstance(value, Mapping):
        type_ = type(value).__name__.capitalize()
        key_type = guess_type(
            next(iter(value.keys())),
            module_name_map=module_name_map,
            known_structs=known_structs,
        )
        value_type = guess_type(
            next(iter(value.values())),
            module_name_map=module_name_map,
            known_structs=known_structs,
        )
        return f"{type_}[{key_type}, {value_type}]"

    if isinstance(value, Collection):
        type_ = type(value).__name__.capitalize()
        item_type = guess_type(
            next(iter(value)),
            module_name_map=module_name_map,
            known_structs=known_structs,
        )
        return f"{type_}[{item_type}]"

    if hasattr(value, "__class__"):
        raw_module = value.__class__.__module__
        class_name: str = value.__class__.__name__
        if raw_module in module_name_map:
            return f"{module_name_map[raw_module]}.{class_name}"
        if type(value) in known_structs:
            return class_name
    return "Any"


def patch_value_repr(  # pylint: disable=too-many-branches
    value, module_name_map: dict[str, str]
) -> Any:
    """
    Patches value representation and adds `module` when applicable.

    This particularly useful for defaults values that uses structs from other modules.
    By default, `thrifpy2` does not include the module name in the default value.

    >>> value
    [Label(name='default', color=3)]
    >>> patch_value_repr(value, module_name_map={'common.labels_thrift': 'labels'})
    >>> value
    [labels.Label(name='default', color=3)]

    """
    if isinstance(value, (bool, int, float, str, bytes, type(None))):
        return value

    if isinstance(value, Collection):
        for x in value:
            patch_value_repr(x, module_name_map=module_name_map)
        return value

    if isinstance(value, Mapping):
        for x in value.values():
            patch_value_repr(x, module_name_map=module_name_map)
        return value

    if value and hasattr(value, "__class__"):
        cls = value.__class__
        raw_module = cls.__module__
        if module := module_name_map.get(raw_module):
            if not hasattr(cls.__repr__, "_patched"):
                cls.__repr__ = _repr_with_module(module)(cls.__repr__)

    return value


def _repr_with_module(module_name: str):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if not result.startswith(f"{module_name}."):
                return f"{module_name}.{result}"
            return result

        setattr(wrapper, "_patched", True)
        return wrapper

    return deco


def get_python_type(ttype: int, meta: list) -> str:
    return TTYPE_MAP[ttype](meta)


def _get_bool(meta: list) -> str:
    del meta
    return "_typedefs.Bool"


def _get_double(meta: list) -> str:
    del meta
    return "_typedefs.Double"


def _get_byte(meta: list) -> str:
    del meta
    return "_typedefs.Byte"


def _get_binary(meta: list) -> str:
    del meta
    return "_typedefs.Binary"


def _get_i16(meta: list) -> str:
    del meta
    return "_typedefs.I16"


def _get_i32(meta: list) -> str:
    if meta and meta[0] is not None:
        return f"{meta[0].__module__}.{meta[0].__name__}"
    return "_typedefs.I32"


def _get_i64(meta: list) -> str:
    del meta
    return "_typedefs.I64"


def _get_str(meta: list) -> str:
    del meta
    return "_typedefs.String"


def _get_struct(meta: list) -> str:
    return f"{meta[0].__module__}.{meta[0].__name__}"


def _get_list(meta: list) -> str:
    subttype, submeta = _unpack_meta(meta)
    return f"List[{get_python_type(subttype, submeta)}]"


def _get_map(meta: list) -> str:
    key, value = meta[0]
    key_ttype, key_meta = _unpack_meta([key])
    value_ttype, value_meta = _unpack_meta([value])
    key_pytype = get_python_type(key_ttype, key_meta)
    value_pytype = get_python_type(value_ttype, value_meta)
    return f"Dict[{key_pytype}, {value_pytype}]"


def _get_set(meta: list) -> str:
    subttype, submeta = _unpack_meta(meta)
    return f"Set[{get_python_type(subttype, submeta)}]"


def _unpack_meta(meta: list) -> tuple[int, list]:
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
