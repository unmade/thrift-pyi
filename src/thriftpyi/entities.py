from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Sequence, Type, Union

if TYPE_CHECKING:
    AnyAssign = Union[ast.Assign, ast.AnnAssign]
    AnyFunctionDef = Union[ast.AsyncFunctionDef, ast.FunctionDef]
    AnyFunctionDefType = Union[Type[ast.AsyncFunctionDef], Type[ast.FunctionDef]]


FieldValue = Union[str, int, bool, None]


@dataclass
class ModuleItem:
    name: str
    fields: List[Field] = field(default_factory=list)
    methods: List[Method] = field(default_factory=list)

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
    ):
        bases = bases or []
        decorators = decorators or []

        body: List[ast.stmt] = []
        body.extend(entry.as_ast() for entry in self.fields)
        body.extend(entry.as_ast() for entry in self.methods)

        if not body:
            body = [ast.Expr(value=ast.Constant(value=Ellipsis))]

        return ast.ClassDef(
            name=self.name,
            bases=[[ast.Name(id=base, ctx=ast.Load())] for base in bases],
            keywords=[],
            body=body,
            decorator_list=[
                ast.Name(id=decorator, ctx=ast.Load()) for decorator in decorators
            ],
        )


@dataclass
class Method:
    name: str
    args: List[Field] = field(default_factory=list)
    returns: List[Field] = field(default_factory=list)
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
            args=ast.arguments(
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
    type: str
    value: FieldValue
    required: bool

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
        )

    def as_ast(self) -> AnyAssign:
        if not self.required:
            annotation = ast.Name(id=f"Optional[{self.type}]", ctx=ast.Load())
        else:
            annotation = ast.Name(id=self.type, ctx=ast.Load())

        if self.required and self.value is None:
            value = None
        else:
            value = ast.Constant(value=self.value, kind=None)

        return ast.AnnAssign(
            target=ast.Name(id=self.name, ctx=ast.Store()),
            annotation=annotation,
            value=value,
            simple=1,
        )
