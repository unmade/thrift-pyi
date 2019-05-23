from types import ModuleType
from typing import Dict, List, Optional, Tuple

from thriftpy2.thrift import TPayloadMeta, TType


class InterfaceProxy:
    def __init__(self, module: ModuleType):
        self.module = module

    def get_services(self) -> List["ServiceProxy"]:
        return [
            ServiceProxy(member)
            for member in self.module.__dict__.values()
            if hasattr(member, "thrift_services")
        ]

    def get_imports(self) -> Dict[str, ModuleType]:
        return {
            name: item
            for name, item in self.module.__dict__.items()
            if isinstance(item, ModuleType)
        }

    def get_errors(self) -> List["ExceptionProxy"]:
        return [
            ExceptionProxy(member)
            for name, member in self.module.__dict__.items()
            if isinstance(member, TPayloadMeta) and hasattr(member, "args")
        ]

    def get_enums(self) -> List["EnumProxy"]:
        return [
            EnumProxy(member)
            for name, member in self.module.__dict__.items()
            if hasattr(member, "_NAMES_TO_VALUES")
        ]

    def get_structs(self) -> List["StructProxy"]:
        return [
            StructProxy(member)
            for name, member in self.module.__dict__.items()
            if isinstance(member, TPayloadMeta) and not hasattr(member, "args")
        ]


class StructProxy:
    def __init__(self, tstruct: TPayloadMeta):
        self._tstruct = tstruct
        self.name = tstruct.__name__
        self.module_name = tstruct.__module__

    def get_fields(self) -> List["FieldProxy"]:
        default_spec = dict(self._tstruct.default_spec)
        return [
            FieldProxy(thrift_spec, default_value=default_spec[thrift_spec[1]])
            for thrift_spec in self._tstruct.thrift_spec.values()
        ]


class ExceptionProxy:
    def __init__(self, texc: TPayloadMeta):
        self._texc = texc
        self.name = texc.__name__
        self.module_name = texc.__module__

    def get_fields(self) -> List["FieldProxy"]:
        default_spec = dict(self._texc.default_spec)
        return [
            FieldProxy(thrift_spec, default_value=default_spec[thrift_spec[1]])
            for thrift_spec in self._texc.thrift_spec.values()
        ]


class EnumFieldProxy:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class EnumProxy:
    def __init__(self, tenum: TPayloadMeta):
        self._tenum = tenum
        self.name = tenum.__name__
        self.module_name = tenum.__module__

    def get_fields(self) -> List["EnumFieldProxy"]:
        fields = self._tenum._NAMES_TO_VALUES  # pylint: disable=protected-access
        return [EnumFieldProxy(name, value) for name, value in fields.items()]


class ServiceProxy:
    def __init__(self, service):
        self.service = service
        self.name = service.__name__
        self.module_name = service.__module__

    def get_methods(self) -> List[str]:
        return [name for name in self.service.thrift_services]

    def get_args_for(self, method_name) -> List["VarProxy"]:
        method_args = getattr(self.service, f"{method_name}_args").thrift_spec.values()
        return [VarProxy(arg) for arg in method_args]

    def get_return_type_for(self, method_name) -> str:
        returns = getattr(self.service, f"{method_name}_result").thrift_spec.get(0)
        if returns is None:
            return "None"
        return VarProxy(returns).reveal_type_for(self.module_name)


class VarProxy:
    def __init__(self, thrift_spec: tuple):
        ttype, name, *meta, _ = thrift_spec
        self._ttype: int = ttype
        self.name: str = name
        self._meta = meta
        self._is_required: bool = True

    def reveal_type_for(self, module_name: str) -> str:
        pytype = _get_python_type(self._ttype, self._is_required, self._meta)
        start, _, end = pytype.rpartition(f"{module_name}.")
        return start + end


class FieldProxy(VarProxy):
    def __init__(self, thrift_spec: tuple, default_value):
        super().__init__(thrift_spec)
        self._is_required = thrift_spec[-1] or default_value is not None
        self._has_default_value = not thrift_spec[-1]
        self._default_value = default_value

    def reveal_value(self) -> Optional[str]:
        if self._has_default_value:
            return f"{self._default_value}"
        return None


def _get_python_type(ttype: int, is_required: bool, meta: List) -> str:
    type_map = {
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
    pytype = type_map[ttype](meta)
    if not is_required:
        pytype = f"Optional[{pytype}]"
    return pytype


def _get_bool(meta: List) -> str:
    del meta
    return "bool"


def _get_double(meta: List) -> str:
    del meta
    return "float"


def _get_byte(meta: List) -> str:
    del meta
    return "int"


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
    return f"List[{_get_python_type(subttype, True, submeta)}]"


def _get_map(meta: List) -> str:
    key, value = meta[0]
    key_ttype, key_meta = _unpack_meta([key])
    value_ttype, value_meta = _unpack_meta([value])
    key_pytype = _get_python_type(key_ttype, True, key_meta)
    value_pytype = _get_python_type(value_ttype, True, value_meta)
    return f"Dict[{key_pytype}, {value_pytype}]"


def _get_set(meta: List) -> str:
    subttype, submeta = _unpack_meta(meta)
    return f"Set[{_get_python_type(subttype, True, submeta)}]"


def _unpack_meta(meta: List) -> Tuple[int, List]:
    try:
        subttype, submeta = meta[0]
    except TypeError:
        subttype, submeta = meta[0], None
    return subttype, [submeta]
