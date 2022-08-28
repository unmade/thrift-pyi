from __future__ import annotations

import ast
from typing import List, Optional, Type, Union

from thriftpyi.proxies import ClassProxy, InterfaceProxy, NoDefault, ServiceProxy

AnyFunctionDef = Union[Type[ast.AsyncFunctionDef], Type[ast.FunctionDef]]


def make_init_module(imports: List[str]) -> ast.Module:
    return ast.Module(
        body=[
            ast.ImportFrom(
                module=None,
                names=[ast.alias(name=name, asname=None) for name in sorted(imports)],
                level=1,
            )
        ],
        type_ignores=[],
    )


def make_module(
    interface: InterfaceProxy, is_async: bool, strict_optional: bool
) -> ast.Module:
    return ast.Module(
        body=[
            *make_imports(interface),
            *make_exceptions(interface, strict_optional),
            *make_enums(interface),
            *make_structs(interface, strict_optional),
            *make_service(interface, is_async),
        ],
        type_ignores=[],
    )


def make_imports(interface: InterfaceProxy) -> List[ast.ImportFrom]:
    imports = []
    if interface.get_structs():
        imports.append(
            ast.ImportFrom(
                module="dataclasses",
                names=[ast.alias(name="dataclass", asname=None)],
                level=0,
            )
        )
    if interface.get_enums():
        imports.append(
            ast.ImportFrom(
                module="enum", names=[ast.alias(name="IntEnum", asname=None)], level=0
            )
        )

    imports.append(
        ast.ImportFrom(
            module="typing", names=[ast.alias(name="*", asname=None)], level=0
        )
    )

    imports.extend(
        ast.ImportFrom(module=None, names=[ast.alias(name=name, asname=None)], level=1)
        for name in sorted(interface.get_imports())
    )

    return imports


def make_exceptions(interface: InterfaceProxy, strict_optional) -> List[ast.ClassDef]:
    return [
        ast.ClassDef(
            name=error.name,
            bases=[ast.Name(id="Exception", ctx=ast.Load())],
            keywords=[],
            body=make_exception_body(error, strict_optional),
            decorator_list=[],
        )
        for error in interface.get_errors()
    ]


def make_exception_body(error: ClassProxy, strict_optional):
    if not error.get_fields():
        return [ast.Ellipsis()]
    return [
        ast.FunctionDef(
            name="__init__",
            args=ast.arguments(
                posonlyargs=[],
                args=[
                    ast.arg(arg="self", annotation=None),
                    *[
                        ast.arg(
                            arg=field.name,
                            annotation=ast.Name(
                                id=field.reveal_type_for(
                                    error.module_name, strict_optional
                                ),
                                ctx=ast.Load(),
                            ),
                        )
                        for field in error.get_fields()
                    ],
                ],
                vararg=[],
                kwarg=[],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[
                    make_struct_field_value(field.reveal_value(strict_optional))
                    for field in error.get_fields()
                    if field is not None
                ],
            ),
            body=[ast.Ellipsis()],
            decorator_list=[],
            lineno=0,
        )
    ]


def make_enums(interface: InterfaceProxy):
    return [
        ast.ClassDef(
            name=enum_.name,
            bases=[ast.Name(id="IntEnum", ctx=ast.Load())],
            keywords=[],
            body=[
                ast.Assign(
                    targets=[ast.Name(id=field.name, ctx=ast.Store())],
                    value=ast.Constant(value=field.reveal_value(), kind=None),
                    lineno=0,
                )
                for field in enum_.get_fields()
            ],
            decorator_list=[],
        )
        for enum_ in interface.get_enums()
    ]


def make_structs(interface: InterfaceProxy, strict_optional) -> List[ast.ClassDef]:
    return [
        ast.ClassDef(
            name=struct.name,
            bases=[],
            keywords=[],
            body=make_struct_body(struct, strict_optional),
            decorator_list=[ast.Name(id="dataclass", ctx=ast.Load())],
        )
        for struct in interface.get_structs()
    ]


def make_struct_body(struct: ClassProxy, strict_optional):
    if not struct.get_fields():
        return [ast.Ellipsis()]
    return [
        ast.AnnAssign(
            target=ast.Name(id=field.name, ctx=ast.Store()),
            annotation=ast.Name(
                id=field.reveal_type_for(struct.module_name, strict_optional),
                ctx=ast.Load(),
            ),
            value=make_struct_field_value(field.reveal_value(strict_optional)),
            simple=1,
        )
        for field in struct.get_fields()
    ]


def make_struct_field_value(value) -> Optional[ast.Constant]:
    if value is NoDefault:
        return None
    return ast.Constant(value=value, kind=None)


def make_service(interface: InterfaceProxy, is_async: bool):
    return [
        ast.ClassDef(
            name=service.name,
            bases=[],
            keywords=[],
            body=make_service_body(service, is_async),
            decorator_list=[],
        )
        for service in interface.get_services()
    ]


def make_service_body(service: ServiceProxy, is_async: bool):
    if not service.get_methods():
        return [ast.Ellipsis()]

    node: AnyFunctionDef = ast.FunctionDef
    if is_async:
        node = ast.AsyncFunctionDef

    return [
        node(
            name=method_name,
            args=ast.arguments(
                posonlyargs=[],
                args=[
                    ast.arg(arg="self", annotation=None),
                    *[
                        ast.arg(
                            arg=param.name,
                            annotation=ast.Name(
                                id=param.reveal_type_for(service.module_name),
                                ctx=ast.Load(),
                            ),
                        )
                        for param in service.get_args_for(method_name)
                    ],
                ],
                vararg=[],
                kwarg=[],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
            ),
            body=[ast.Ellipsis()],
            decorator_list=[],
            returns=ast.Name(
                id=service.get_return_type_for(method_name), ctx=ast.Load()
            ),
            lineno=0,
        )
        for method_name in service.get_methods()
    ]
