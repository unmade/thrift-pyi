import subprocess
from pathlib import Path
from typing import List

from thriftpyi import factories, files, renderers
from thriftpyi.entities import Content


def thriftpyi(
    interfaces_dir: str, output_dir: str, is_async: bool, strict_optional: bool
) -> None:
    interfaces = files.list_interfaces(interfaces_dir)
    _generate_stubs(interfaces, output_dir, is_async, strict_optional)
    _generate_init(interfaces, output_dir)
    path = Path(output_dir).resolve()
    subprocess.check_call([f"autoflake -i -r {path.joinpath('*')}"], shell=True)
    subprocess.check_call(["black", "--quiet", f"{path}"])


def _generate_stubs(
    interfaces: List[str], output_dir: str, is_async: bool, strict_optional: bool
) -> None:
    for interface in interfaces:
        _generate(
            factories.make_content(interface, is_async, strict_optional),
            interface,
            output_dir,
        )


def _generate_init(interfaces: List[str], output_dir: str) -> None:
    imports = sorted([files.get_name(interface) for interface in interfaces])
    _generate(Content(imports=imports), "__init__.pyi", output_dir)


def _generate(content: Content, interface: str, output_dir: str) -> None:
    result = renderers.render(content)
    files.save(result, to=files.build_output_path(interface, output_dir))
