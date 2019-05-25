from typing import List

import thriftpy2 as thriftpy
from thriftpyi.entities import Class, Content, Field, Method, Service
from thriftpyi.proxies import InterfaceProxy


def parse(interface: str) -> Content:
    module = InterfaceProxy(thriftpy.load(interface))
    return Content(
        imports=parse_imports(module),
        errors=parse_errors(module),
        enums=parse_enums(module),
        structs=parse_structs(module),
        services=parse_services(module),
    )


def parse_imports(module: InterfaceProxy) -> List[str]:
    return list(module.get_imports().keys())


def parse_errors(module: InterfaceProxy) -> List[Class]:
    return [
        Class(
            name=error.name,
            fields=[
                Field(
                    name=field.name,
                    type=field.reveal_type_for(error.module_name),
                    value=field.reveal_value(),
                )
                for field in error.get_fields()
            ],
        )
        for error in module.get_errors()
    ]


def parse_enums(module: InterfaceProxy) -> List[Class]:
    return [
        Class(
            name=enum.name,
            fields=[
                Field(
                    name=field.name,
                    type=field.reveal_type_for(enum.module_name),
                    value=field.reveal_value(),
                )
                for field in enum.get_fields()
            ],
        )
        for enum in module.get_enums()
    ]


def parse_structs(module: InterfaceProxy) -> List[Class]:
    return [
        Class(
            name=struct.name,
            fields=[
                Field(
                    name=field.name,
                    type=field.reveal_type_for(struct.module_name),
                    value=field.reveal_value(),
                )
                for field in struct.get_fields()
            ],
        )
        for struct in module.get_structs()
    ]


def parse_services(module: InterfaceProxy) -> List[Service]:
    return [
        Service(
            name=service.name,
            methods=[
                Method(
                    name=method_name,
                    args=[
                        Field(
                            name=arg.name, type=arg.reveal_type_for(service.module_name)
                        )
                        for arg in service.get_args_for(method_name)
                    ],
                    return_type=service.get_return_type_for(method_name),
                )
                for method_name in service.get_methods()
            ],
        )
        for service in module.get_services()
    ]
