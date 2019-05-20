from types import ModuleType
from typing import Dict, List

from thriftpy2.thrift import TPayloadMeta, TType


class InterfaceProxy:
    def __init__(self, module: ModuleType):
        self.module = module

    def get_service(self) -> "ServiceProxy":
        return ServiceProxy(
            [
                member
                for member in self.module.__dict__.values()
                if hasattr(member, "thrift_services")
            ][0]
        )

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

    def get_fields(self) -> List["VarProxy"]:
        return [
            VarProxy(thrift_spec) for thrift_spec in self._tstruct.thrift_spec.values()
        ]


class ExceptionProxy:
    def __init__(self, texc: TPayloadMeta):
        self._texc = texc
        self.name = texc.__name__

    def get_fields(self) -> List["FieldProxy"]:
        return [
            FieldProxy(thrift_spec) for thrift_spec in self._texc.thrift_spec.values()
        ]


class EnumFieldProxy:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class EnumProxy:
    def __init__(self, tenum: TPayloadMeta):
        self._tenum = tenum
        self.name = tenum.__name__

    def get_fields(self) -> List["EnumFieldProxy"]:
        fields = self._tenum._NAMES_TO_VALUES  # pylint: disable=protected-access
        return [EnumFieldProxy(name, value) for name, value in fields.items()]


class ServiceProxy:
    def __init__(self, service):
        self.service = service

    @property
    def name(self):
        return self.service.__name__

    def get_methods(self) -> List[str]:
        return [name for name in self.service.thrift_services]

    def get_args_for(self, method_name) -> List["VarProxy"]:
        method_args = getattr(self.service, f"{method_name}_args").thrift_spec.values()
        return [VarProxy(arg) for arg in method_args]

    def get_return_type_for(self, method_name) -> str:
        returns = getattr(self.service, f"{method_name}_result").thrift_spec.get(0)
        if returns is None:
            return "None"
        return VarProxy(returns).reveal_type()


class VarProxy:
    def __init__(self, thrift_spec: tuple):
        ttype, name, *meta, _ = thrift_spec
        self._ttype: int = ttype
        self.name: str = name
        self._meta = meta
        self._is_required: bool = True

    def reveal_type(self) -> str:
        return _get_python_type(self._ttype, self._is_required, self._meta)


class FieldProxy(VarProxy):
    def __init__(self, thrift_spec: tuple):
        super().__init__(thrift_spec)
        self._is_required = thrift_spec[-1]


def _get_python_type(ttype: int, is_required: bool, meta=None) -> str:
    type_map = {
        TType.BOOL: "bool",
        TType.DOUBLE: "float",
        TType.BYTE: "int",
        TType.I16: "int",
        TType.I32: "int",
        TType.I64: "int",
        TType.STRING: "str",
        TType.STRUCT: "Any",
        TType.MAP: "dict",
        TType.SET: "set",
        TType.LIST: "list",
    }
    pytype = type_map.get(ttype, "Any")
    if meta:
        subtype = meta[0]
        if ttype == TType.STRUCT:
            pytype = subtype.__name__
        if ttype == TType.LIST:
            try:
                subtype, meta = subtype
            except TypeError:
                meta = None
            pytype = f"List[{_get_python_type(subtype, True, [meta])}]"
    if not is_required:
        pytype = f"Optional[{pytype}]"
    return pytype
