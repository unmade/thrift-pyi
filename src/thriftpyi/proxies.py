from types import ModuleType
from typing import Dict, List, Optional, cast

import thriftpy2
from thriftpy2.thrift import TPayloadMeta

from thriftpyi.utils import get_python_type


class InterfaceProxy:
    def __init__(self, interface_path: str):
        self.module = thriftpy2.load(interface_path)

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

    def get_errors(self) -> List["ClassProxy"]:
        return [
            ClassProxy(member)
            for name, member in self.module.__dict__.items()
            if isinstance(member, TPayloadMeta) and hasattr(member, "args")
        ]

    def get_enums(self) -> List["EnumProxy"]:
        return [
            EnumProxy(member)
            for name, member in self.module.__dict__.items()
            if hasattr(member, "_NAMES_TO_VALUES")
        ]

    def get_structs(self) -> List["ClassProxy"]:
        return [
            ClassProxy(member)
            for name, member in self.module.__dict__.items()
            if isinstance(member, TPayloadMeta) and not hasattr(member, "args")
        ]


class ClassProxy:
    def __init__(self, tclass: TPayloadMeta):
        self._tclass = tclass
        self.name = tclass.__name__
        self.module_name = tclass.__module__

    def get_fields(self) -> List["FieldProxy"]:
        default_spec = dict(self._tclass.default_spec)
        return [
            FieldProxy(thrift_spec, default_spec=default_spec)
            for thrift_spec in self._tclass.thrift_spec.values()
        ]


class EnumProxy(ClassProxy):
    def get_fields(self) -> List["FieldProxy"]:
        fields = self._tclass._NAMES_TO_VALUES  # pylint: disable=protected-access
        ttype = self._tclass._ttype  # pylint: disable=protected-access
        return [
            FieldProxy((ttype, name, True), default_spec={name: value})
            for name, value in fields.items()
        ]


class ServiceProxy:
    def __init__(self, service):
        self.service = service
        self.name = service.__name__
        self.module_name = service.__module__

    def get_methods(self) -> List[str]:
        return cast(List[str], self.service.thrift_services[:])

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

    def reveal_type_for(self, module_name: str, strict_optional: bool = True) -> str:
        pytype = get_python_type(
            self._ttype, self._is_required and strict_optional, self._meta
        )
        start, _, end = pytype.rpartition(f"{module_name}.")
        return start + end


class FieldProxy(VarProxy):
    def __init__(self, thrift_spec: tuple, default_spec: Dict[str, str]):
        super().__init__(thrift_spec)
        self._default_value = default_spec[self.name]
        self._is_required = thrift_spec[-1]

    def reveal_value(self, strict_optional: bool = True) -> Optional[str]:
        if (
            self._default_value is not None
            or not self._is_required
            or not strict_optional
        ):
            if isinstance(self._default_value, str):
                return f'"{self._default_value}"'
            return f"{self._default_value}"
        return None
