from __future__ import annotations

import ast
from typing import TYPE_CHECKING, Iterable, List

if TYPE_CHECKING:
    from thriftpyi.proxies import TModuleProxy


def build(
    proxy: TModuleProxy, is_async: bool, strict_fields: bool, strict_methods: bool
) -> ast.Module:
    return ast.Module(
        body=[
            *_make_imports(proxy),
            *_make_exceptions(proxy, strict=strict_fields),
            *_make_enums(proxy),
            *_make_structs(proxy, strict=strict_fields),
            *_make_service(proxy, is_async, strict=strict_methods),
        ],
        type_ignores=[],
    )


def build_init(imports: Iterable[str]) -> ast.Module:
    return ast.Module(
        body=[_make_relative_import(imports)],
        type_ignores=[],
    )


def _make_imports(proxy: TModuleProxy) -> List[ast.ImportFrom]:
    imports = []
    if proxy.has_structs():
        imports.append(_make_absolute_import("dataclasses", "dataclass"))
    if proxy.has_enums():
        imports.append(_make_absolute_import("enum", "IntEnum"))

    imports.append(_make_absolute_import("typing", "*"))
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


def _make_exceptions(interface: TModuleProxy, strict: bool) -> List[ast.ClassDef]:
    return [
        item.with_options(ignore_required=not strict).as_ast(bases=["Exception"])
        for item in interface.get_exceptions()
    ]


def _make_enums(interface: TModuleProxy) -> List[ast.ClassDef]:
    return [item.as_ast(bases=["IntEnum"]) for item in interface.get_enums()]


def _make_structs(interface: TModuleProxy, strict: bool) -> List[ast.ClassDef]:
    return [
        item.with_options(ignore_required=not strict).as_ast(decorators=["dataclass"])
        for item in interface.get_structs()
    ]


def _make_service(
    interface: TModuleProxy, is_async: bool, strict: bool
) -> List[ast.ClassDef]:
    services = interface.get_services()

    return [
        item.with_options(ignore_optional=strict, is_async=is_async).as_ast()
        for item in services
    ]
