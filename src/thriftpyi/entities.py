from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import (
    TYPE_CHECKING,
    MutableMapping,
    MutableSequence,
    MutableSet,
    Sequence,
    Type,
    Union,
)

if TYPE_CHECKING:
    AnyFunctionDef = Union[ast.AsyncFunctionDef, ast.FunctionDef]
    AnyFunctionDefType = Union[Type[ast.AsyncFunctionDef], Type[ast.FunctionDef]]


FieldValue = Union[str, int, bool, None]


@dataclass
class ModuleItem:
    name: str
    fields: list[Field] = field(default_factory=list)
    methods: list[Method] = field(default_factory=list)

    def with_options(
        self,
        *,
        ignore_optional: bool = False,
        ignore_required: bool = False,
        is_async: bool = False,
    ) -> ModuleItem:
        return self.__class__(
            name=self.name,
            fields=[
                field.with_options(
                    ignore_optional=ignore_optional,
                    ignore_required=ignore_required,
                )
                for field in self.fields
            ],
            methods=[
                method.with_options(
                    ignore_optional=ignore_optional,
                    ignore_required=ignore_required,
                    is_async=is_async,
                )
                for method in self.methods
            ],
        )

    def as_ast(
        self,
        *,
        bases: Sequence[str] = None,
        decorators: Sequence[str] = None,
    ) -> ast.ClassDef:
        bases = bases or []
        decorators = decorators or []

        body: list[ast.stmt] = []
        body.extend(entry.as_ast() for entry in self.fields)
        body.extend(entry.as_ast() for entry in self.methods)

        if not body:
            body = [ast.Expr(value=ast.Constant(value=Ellipsis))]

        return ast.ClassDef(
            name=self.name,
            bases=[ast.Name(id=base, ctx=ast.Load()) for base in bases],
            keywords=[],
            body=body,
            decorator_list=[
                ast.Name(id=decorator, ctx=ast.Load()) for decorator in decorators
            ],
        )


@dataclass
class Method:
    name: str
    args: list[Field] = field(default_factory=list)
    returns: list[Field] = field(default_factory=list)
    is_async: bool = False

    def with_options(
        self,
        *,
        ignore_optional: bool = False,
        ignore_required: bool = False,
        is_async: bool = False,
    ) -> Method:
        return self.__class__(
            name=self.name,
            args=[
                entry.with_options(
                    ignore_optional=ignore_optional,
                    ignore_required=ignore_required,
                )
                for entry in self.args
            ],
            returns=[
                entry.with_options(
                    ignore_optional=ignore_optional,
                    ignore_required=ignore_required,
                )
                for entry in self.returns
            ],
            is_async=is_async,
        )

    def as_ast(self) -> AnyFunctionDef:
        factory: AnyFunctionDefType = ast.FunctionDef
        if self.is_async:
            factory = ast.AsyncFunctionDef

        returns: ast.expr
        if self.returns and self.returns[0].type:
            returns = ast.Name(id=self.returns[0].type, ctx=ast.Load())
        else:
            returns = ast.Constant(value=None, kind=None)

        return factory(
            name=self.name,
            args=ast.arguments(  # type: ignore[call-overload]
                posonlyargs=[],
                args=[
                    ast.arg(arg="self", annotation=None),
                    *[entry.as_ast() for entry in self.args],
                ],
                vararg=[],
                kwarg=[],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
            ),
            body=[ast.Expr(value=ast.Constant(value=Ellipsis))],
            decorator_list=[],
            returns=returns,
            lineno=0,
        )


@dataclass
class Field:
    name: str
    type: str | None
    value: FieldValue
    required: bool
    module: str | None = None

    def with_options(self, *, ignore_optional: bool, ignore_required: bool) -> Field:
        required = self.required
        if ignore_optional and not required:
            required = True
        if ignore_required and required:
            required = False

        return self.__class__(
            name=self.name,
            type=self.type,
            value=self.value,
            required=required,
            module=self.module,
        )

    def as_ast(self) -> ast.AnnAssign | ast.Assign:
        if self.type is None:
            return ast.Assign(
                targets=[ast.Name(id=self.name, ctx=ast.Store())],
                value=self._make_ast_value(),
                lineno=0,
            )

        if not self.required:
            annotation = ast.Name(id=f"Optional[{self.type}]", ctx=ast.Load())
        else:
            annotation = ast.Name(id=self.type, ctx=ast.Load())

        if self.required and self.value is None:
            value = None
        else:
            value = self._make_ast_value()

        return ast.AnnAssign(
            target=ast.Name(id=self.name, ctx=ast.Store()),
            annotation=annotation,
            value=value,
            simple=1,
        )

    def _make_ast_value(self) -> ast.expr:
        if self.module:
            body = ast.parse(f"{self.module}.{self.value}").body
            return body[0].value  # type: ignore[attr-defined, no-any-return]
        return ast.Constant(value=self.value, kind=None)


@dataclass
class StructField(Field):
    def _make_ast_value(self) -> ast.expr:
        if isinstance(self.value, (MutableSequence, MutableSet, MutableMapping)):
            if self.value:
                value = ast.Lambda(
                    args=[], body=ast.Constant(value=self.value, kind=None)
                )
            else:
                value = ast.Name(id=self.value.__class__.__name__, ctx=ast.Load())

            return ast.Call(
                func=ast.Name(id="field", ctx=ast.Load()),
                args=[],
                keywords=[
                    ast.keyword(
                        arg="default_factory",
                        value=value,
                    )
                ],
            )
        return super()._make_ast_value()
