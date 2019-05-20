from types import ModuleType
from typing import List, Optional

import thriftpy2 as thriftpy
from thriftpyi.entities import (
    Arg,
    Content,
    Enumeration,
    EnumField,
    Error,
    Field,
    Method,
    Service,
    Struct,
)
from thriftpyi.proxies import InterfaceProxy, ServiceProxy


def parse(interface: str) -> Content:
    module = InterfaceProxy(thriftpy.load(interface))
    return Content(
        imports=parse_imports(module),
        errors=parse_errors(module),
        enums=parse_enums(module),
        structs=parse_structs(module),
        service=parse_service(module.get_service()),
    )


def parse_imports(module: InterfaceProxy) -> List[str]:
    return [
        name
        for name, item in module.get_imports().items()
        if isinstance(item, ModuleType)
    ]


def parse_errors(module: InterfaceProxy) -> List[Error]:
    return [
        Error(
            name=error.name,
            fields=[
                Field(name=field.name, type=field.reveal_type_for(error.module_name))
                for field in error.get_fields()
            ],
        )
        for error in module.get_errors()
    ]


def parse_enums(module: InterfaceProxy) -> List[Enumeration]:
    return [
        Enumeration(
            name=enum.name,
            fields=[
                EnumField(name=field.name, value=field.value)
                for field in enum.get_fields()
            ],
        )
        for enum in module.get_enums()
    ]


def parse_structs(module: InterfaceProxy) -> List[Struct]:
    return [
        Struct(
            name=struct.name,
            fields=[
                Field(name=field.name, type=field.reveal_type_for(struct.module_name))
                for field in struct.get_fields()
            ],
        )
        for struct in module.get_structs()
    ]


def parse_service(service: Optional[ServiceProxy]) -> Optional[Service]:
    if service is None:
        return None
    return Service(
        name=service.name,
        methods=[
            Method(
                name=method_name,
                args=[
                    Arg(name=arg.name, type=arg.reveal_type_for(service.module_name))
                    for arg in service.get_args_for(method_name)
                ],
                return_type=service.get_return_type_for(method_name),
            )
            for method_name in service.get_methods()
        ],
    )
