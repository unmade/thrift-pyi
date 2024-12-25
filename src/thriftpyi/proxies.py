from __future__ import annotations

from typing import cast

from thriftpyi.entities import Field, FieldValue, Method, ModuleItem, StructField
from thriftpyi.utils import get_python_type, guess_type


class TModuleProxy:
    __slots__ = ["tmodule"]

    def __init__(self, tmodule) -> None:
        self.tmodule = tmodule

    def get_consts(self) -> list[Field]:
        tconsts = (
            (name, value)
            for name, value in vars(self.tmodule).items()
            if value in self.tmodule.__thrift_meta__["consts"]
        )
        return [self._make_const(tconst) for tconst in tconsts]

    def get_enums(self) -> list[ModuleItem]:
        return [
            self._make_enum(tenum) for tenum in self.tmodule.__thrift_meta__["enums"]
        ]

    def get_exceptions(self) -> list[ModuleItem]:
        return [
            self._make_exception(texc)
            for texc in self.tmodule.__thrift_meta__["exceptions"]
        ]

    def get_imports(self) -> list[str]:
        return [item.__name__ for item in self.tmodule.__thrift_meta__["includes"]]

    def get_services(self) -> list[ModuleItem]:
        return [
            self._make_service(tservice)
            for tservice in self.tmodule.__thrift_meta__["services"]
        ]

    def get_structs(self) -> list[ModuleItem]:
        return [
            self._make_struct(tstruct)
            for tstruct in self.tmodule.__thrift_meta__["structs"]
        ]

    def has_structs(self) -> bool:
        return len(self.tmodule.__thrift_meta__["structs"]) > 0

    def has_enums(self) -> bool:
        return len(self.tmodule.__thrift_meta__["enums"]) > 0

    def _make_const(self, tconst) -> Field:
        name, value = tconst

        known_modules = {
            module.__name__ for module in self.tmodule.__thrift_meta__["includes"]
        }

        module_name = None
        if hasattr(value, "__class__"):
            module_name = value.__class__.__module__
            if module_name not in known_modules:
                module_name = None

        return Field(
            name=name,
            type=guess_type(
                value,
                known_modules=known_modules,
                known_structs=self.tmodule.__thrift_meta__["structs"],
            ),
            value=value,
            module=module_name,
            required=True,
        )

    @staticmethod
    def _make_enum(tenum) -> ModuleItem:
        fields = tenum._NAMES_TO_VALUES  # pylint: disable=protected-access
        ttype = tenum._ttype  # pylint: disable=protected-access
        tspec = {idx: (ttype, name, True) for idx, name in enumerate(fields)}
        spec = TSpecProxy(
            module_name=tenum.__module__,
            thrift_spec=tspec,
            default_spec=fields,
        )
        return ModuleItem(name=tenum.__name__, fields=spec.get_fields(ignore_type=True))

    @staticmethod
    def _make_exception(texc) -> ModuleItem:
        spec = TSpecProxy(
            module_name=texc.__module__,
            thrift_spec=texc.thrift_spec,
            default_spec=dict(texc.default_spec),
        )

        fields = spec.get_fields()
        methods = []
        if fields:
            methods.append(Method(name="__init__", args=fields))

        return ModuleItem(name=texc.__name__, methods=methods, fields=fields)

    @staticmethod
    def _make_service(tservice) -> ModuleItem:
        return ModuleItem(
            name=tservice.__name__,
            methods=[
                Method(
                    name=method_name,
                    args=TSpecProxy(
                        module_name=tservice.__module__,
                        thrift_spec=getattr(
                            tservice, f"{method_name}_args"
                        ).thrift_spec,
                        default_spec=dict(
                            getattr(tservice, f"{method_name}_args").default_spec
                        ),
                    ).get_fields(),
                    returns=TSpecProxy(
                        module_name=tservice.__module__,
                        thrift_spec=getattr(
                            tservice, f"{method_name}_result"
                        ).thrift_spec,
                        default_spec=dict(
                            getattr(tservice, f"{method_name}_args").default_spec
                        ),
                    ).get_fields(),
                )
                for method_name in tservice.thrift_services
            ],
        )

    @staticmethod
    def _make_struct(tclass) -> ModuleItem:
        spec = TStructSpecProxy(
            module_name=tclass.__module__,
            thrift_spec=tclass.thrift_spec,
            default_spec=dict(tclass.default_spec),
        )
        return ModuleItem(
            name=tclass.__name__,
            fields=spec.get_fields(),
        )


class TSpecItemProxy:
    __slots__ = ("ttype", "name", "meta", "required")

    def __init__(self, item: tuple):
        ttype, name, *meta, required = item
        self.ttype = ttype
        self.name = name
        self.meta = meta
        self.required = required


class TSpecProxy:
    __slots__ = ("module_name", "thrift_spec", "default_spec")

    def __init__(self, module_name: str, thrift_spec, default_spec):
        self.module_name = module_name
        self.thrift_spec = [TSpecItemProxy(thrift_spec[k]) for k in sorted(thrift_spec)]
        self.default_spec = default_spec

    def get_fields(self, *, ignore_type: bool = False) -> list[Field]:
        return [
            Field(
                name=item.name,
                type=self._get_python_type(item) if not ignore_type else None,
                value=self._get_default_value(item),
                required=item.required,
            )
            for item in self.thrift_spec
        ]

    def _remove_self_module(self, pytype: str) -> str:
        left_type, sep, right_type = pytype.partition(",")
        # Due to complex type, such as Dict[some_module.TypeA, some_module.TypeB]
        # recursively deal with the first and second parts
        if right_type != "":
            return (
                self._remove_self_module(left_type)
                + sep
                + self._remove_self_module(right_type)
            )
        start, _, end = pytype.rpartition(f"{self.module_name}.")
        return start + end

    def _get_python_type(self, item: TSpecItemProxy) -> str:
        pytype = get_python_type(item.ttype, meta=item.meta)
        return self._remove_self_module(pytype)

    def _get_default_value(self, item: TSpecItemProxy) -> FieldValue:
        default_value = self.default_spec.get(item.name)
        return cast(FieldValue, default_value)


class TStructSpecProxy(TSpecProxy):
    def get_fields(self, *, ignore_type: bool = False) -> list[Field]:
        return [
            StructField(
                name=item.name,
                type=self._get_python_type(item) if not ignore_type else None,
                value=self._get_default_value(item),
                required=item.required,
            )
            for item in self.thrift_spec
        ]
