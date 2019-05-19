import subprocess
from pathlib import Path

from thriftpyi import files, parsers, renderers


def thriftpyi(interfaces_dir: str, output_dir: str) -> None:
    interfaces = files.list_interfaces(interfaces_dir)
    for interface in interfaces:
        result = renderers.render(parsers.parse(interface))
        files.save(result, to=files.build_output_path(interface, output_dir))
    subprocess.check_call(["black", f"{Path(output_dir).resolve()}"])
