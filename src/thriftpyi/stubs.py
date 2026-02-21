from __future__ import annotations

import ast
from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from thriftpyi.proxies import TModuleProxy


def build(  # pylint: disable=too-many-arguments
    *,
    proxy: TModuleProxy,
    is_async: bool,
    strict_fields: bool,
    strict_methods: bool,
    frozen: bool = False,
    kw_only: bool = False,
) -> ast.Module:
    return ast.Module(
        body=[
            *_make_imports(proxy),
            *_make_exceptions(proxy, strict=strict_fields),
            *_make_enums(proxy),
            *_make_structs(proxy, strict=strict_fields, frozen=frozen, kw_only=kw_only),
            *_make_consts(proxy),
            *_make_service(proxy, is_async, strict=strict_methods),
        ],
        type_ignores=[],
    )


def build_init(imports: Iterable[str]) -> ast.Module:
    return ast.Module(
        body=[_make_relative_import(imports)],
        type_ignores=[],
    )


def build_typedefs() -> ast.Module:
    types_map = {
        "Binary": ("bytes", "BINARY"),
        "Bool": ("bool", "BOOL"),
        "Byte": ("int", "BYTE"),
        "Double": ("float", "DOUBLE"),
        "I16": ("int", "I16"),
        "I32": ("int", "I32"),
        "I64": ("int", "I64"),
        "String": ("str", "STRING"),
    }

    body: list[ast.stmt] = [
        ast.ImportFrom(
            module="dataclasses",
            names=[ast.alias(name="dataclass")],
            level=0,
        ),
        ast.ImportFrom(
            module="typing",
            names=[ast.alias(name="Annotated")],
            level=0,
        ),
        ast.ClassDef(
            name="Metadata",
            bases=[],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id="thrift_type"),
                    annotation=ast.Name(id="str"),
                    simple=1,
                ),
            ],
            decorator_list=[
                ast.Call(
                    func=ast.Name(id="dataclass"),
                    args=[],
                    keywords=[
                        ast.keyword(
                            arg="frozen",
                            value=ast.Constant(value=True),
                        ),
                    ],
                ),
            ],
        ),
    ]

    for alias, (base_type, thrift_type) in types_map.items():
        assign = ast.Assign(
            targets=[ast.Name(id=alias)],
            value=ast.Subscript(
                value=ast.Name(id="Annotated"),
                slice=ast.Tuple(
                    elts=[
                        ast.Name(id=base_type),
                        ast.Call(
                            func=ast.Name(id="Metadata"),
                            args=[],
                            keywords=[
                                ast.keyword(
                                    arg="thrift_type",
                                    value=ast.Constant(value=thrift_type),
                                ),
                            ],
                        ),
                    ],
                ),
            ),
            lineno=0,
        )
        body.append(assign)

    return ast.Module(body=body, type_ignores=[])


def _make_imports(proxy: TModuleProxy) -> list[ast.ImportFrom]:
    imports = [_make_absolute_import("__future__", "annotations")]

    if proxy.has_structs():
        imports.append(_make_absolute_import("dataclasses", "dataclass, field"))
    if proxy.has_enums():
        imports.append(_make_absolute_import("enum", "IntEnum"))

    imports.append(_make_absolute_import("typing", "*"))
    imports.append(_make_relative_import(["_typedefs"]))
    imports.extend(
        _make_relative_import([name]) for name in sorted(proxy.get_imports())
    )

    return imports


def _make_absolute_import(module: str, name: str) -> ast.ImportFrom:
    return ast.ImportFrom(
        module=module,
        names=[ast.alias(name=name, asname=None)],
        level=0,
    )


def _make_relative_import(names: Iterable[str]) -> ast.ImportFrom:
    return ast.ImportFrom(
        module=None,
        names=[ast.alias(name=name, asname=None) for name in sorted(names)],
        level=1,
    )


def _make_consts(interface: TModuleProxy) -> list[ast.stmt]:
    return [item.as_ast() for item in interface.get_consts()]


def _make_exceptions(interface: TModuleProxy, strict: bool) -> list[ast.ClassDef]:
    return [
        item.with_options(ignore_required=not strict).as_ast(bases=["Exception"])
        for item in interface.get_exceptions()
    ]


def _make_enums(interface: TModuleProxy) -> list[ast.ClassDef]:
    return [item.as_ast(bases=["IntEnum"]) for item in interface.get_enums()]


def _dataclass_decorator(*, frozen: bool, kw_only: bool) -> ast.expr:
    kws = []
    if frozen:
        kws.append(ast.keyword("frozen", ast.Constant(True)))
    if kw_only:
        kws.append(ast.keyword("kw_only", ast.Constant(True)))
    return (
        ast.Name("dataclass", ast.Load())
        if not kws
        else ast.Call(ast.Name("dataclass", ast.Load()), [], kws)
    )


def _make_structs(
    interface: TModuleProxy, strict: bool, frozen: bool = False, kw_only: bool = False
) -> list[ast.ClassDef]:
    return [
        item.with_options(ignore_required=not strict).as_ast(
            decorators=[_dataclass_decorator(frozen=frozen, kw_only=kw_only)]
        )
        for item in interface.get_structs()
    ]


def _make_service(
    interface: TModuleProxy, is_async: bool, strict: bool
) -> list[ast.ClassDef]:
    services = interface.get_services()

    return [
        item.with_options(ignore_optional=strict, is_async=is_async).as_ast()
        for item in services
    ]
