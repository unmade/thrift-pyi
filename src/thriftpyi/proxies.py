from types import ModuleType
from typing import Dict, List

from thriftpy2.thrift import TType


class InterfaceProxy:
    def __init__(self, module: ModuleType):
        self.module = module

    def get_service(self) -> "ServiceProxy":
        return ServiceProxy(
            next(
                member
                for member in self.module.__dict__.values()
                if hasattr(member, "thrift_services")
            )
        )

    def get_imports(self) -> Dict[str, ModuleType]:
        return {
            name: item
            for name, item in self.module.__dict__.items()
            if isinstance(item, ModuleType)
        }


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
        ttype, name, *meta, is_required = thrift_spec
        self._ttype = ttype
        self.name = name
        self._meta = meta
        self._is_required = is_required

    def reveal_type(self) -> str:
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
        return type_map.get(self._ttype, "Any")
