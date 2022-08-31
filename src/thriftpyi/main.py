from __future__ import annotations

import subprocess
from pathlib import Path

import thriftpy2

from thriftpyi import files, stubs
from thriftpyi.compat import ast_unparse
from thriftpyi.proxies import TModuleProxy


def thriftpyi(  # pylint: disable=too-many-locals
    interfaces_dir: str,
    output_dir: Path,
    is_async: bool = False,
    strict_fields: bool = False,
    strict_methods: bool = True,
) -> None:
    output_dir = output_dir.resolve()
    interfaces = files.list_interfaces(interfaces_dir)

    stub = stubs.build_init(path.stem for path in interfaces)
    files.save(ast_unparse(stub), to=output_dir / "__init__.pyi")

    for path in interfaces:
        tmodule = thriftpy2.load(str(path))
        proxy = TModuleProxy(tmodule)
        stub = stubs.build(
            proxy,
            is_async=is_async,
            strict_fields=strict_fields,
            strict_methods=strict_methods,
        )
        files.save(ast_unparse(stub), to=output_dir / path.with_suffix(".pyi").name)

    lint(output_dir)


def lint(output_dir: Path) -> None:
    subprocess.check_call([f"autoflake -i -r {output_dir.joinpath('*')}"], shell=True)
    subprocess.check_call(
        ["black", "--pyi", "--quiet", *list(output_dir.glob("*.pyi"))]
    )
