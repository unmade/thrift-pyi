from thriftpyi.entities import Class, Content, Field, Method, Service
from thriftpyi.proxies import ClassProxy, FieldProxy, InterfaceProxy, ServiceProxy


def make_content(interface: str, is_async: bool, strict_optional: bool) -> Content:
    module = InterfaceProxy(interface)
    return Content(
        imports=list(module.get_imports().keys()),
        errors=[make_class(klass, strict_optional) for klass in module.get_errors()],
        enums=[make_class(klass, strict_optional) for klass in module.get_enums()],
        structs=[make_class(klass, strict_optional) for klass in module.get_structs()],
        services=[make_service(service) for service in module.get_services()],
        is_async=is_async,
    )


def make_class(klass: ClassProxy, strict_optional: bool) -> Class:
    return Class(
        name=klass.name,
        fields=[
            make_field(field, klass.module_name, strict_optional)
            for field in klass.get_fields()
        ],
    )


def make_field(field: FieldProxy, module_name: str, strict_optional: bool) -> Field:
    return Field(
        name=field.name,
        type=field.reveal_type_for(module_name, strict_optional),
        value=field.reveal_value(strict_optional),
    )


def make_service(service: ServiceProxy) -> Service:
    return Service(
        name=service.name,
        methods=[
            make_method(method_name, service) for method_name in service.get_methods()
        ],
    )


def make_method(method_name: str, service: ServiceProxy):
    return Method(
        name=method_name,
        args=[
            Field(name=arg.name, type=arg.reveal_type_for(service.module_name))
            for arg in service.get_args_for(method_name)
        ],
        return_type=service.get_return_type_for(method_name),
    )
