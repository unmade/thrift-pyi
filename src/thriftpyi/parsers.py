from types import ModuleType
from typing import List

import thriftpy2 as thriftpy
from thriftpyi.entities import Arg, Content, Method, Service
from thriftpyi.proxies import InterfaceProxy, ServiceProxy


def parse(interface: str) -> Content:
    module = InterfaceProxy(thriftpy.load(interface))
    return Content(
        imports=parse_imports(module), service=parse_service(module.get_service())
    )


def parse_imports(module: InterfaceProxy) -> List[str]:
    return [
        name
        for name, item in module.get_imports().items()
        if isinstance(item, ModuleType)
    ]


def parse_service(service: ServiceProxy) -> Service:
    return Service(
        name=service.name,
        methods=[
            Method(
                name=method_name,
                args=[
                    Arg(name=arg.name, type=arg.reveal_type())
                    for arg in service.get_args_for(method_name)
                ],
                return_type=service.get_return_type_for(method_name),
            )
            for method_name in service.get_methods()
        ],
    )
