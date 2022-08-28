import subprocess
from pathlib import Path

from thriftpyi import compat, factories, files
from thriftpyi.proxies import InterfaceProxy


def thriftpyi(
    interfaces_dir: str, output_dir: str, is_async: bool, strict_optional: bool
) -> None:
    interfaces = files.list_interfaces(interfaces_dir)
    for interface in interfaces:
        proxy = InterfaceProxy(interface)
        module = factories.make_module(
            proxy, is_async=is_async, strict_optional=strict_optional
        )
        _save_module(interface, module, output_dir)

    imports = sorted([files.get_name(interface) for interface in interfaces])
    module = factories.make_init_module(imports)
    _save_module("__init__.pyi", module, output_dir)

    path = Path(output_dir).resolve()
    subprocess.check_call([f"autoflake -i -r {path.joinpath('*')}"], shell=True)
    subprocess.check_call(["black", "--pyi", "--quiet", *list(path.glob("*.pyi"))])


def _save_module(name, module, output_dir):
    content = compat.ast_unparse(module)
    files.save(content, to=files.build_output_path(name, output_dir))
