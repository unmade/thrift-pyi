import os
from pathlib import Path
from typing import List


def save(data: str, to: str) -> None:
    Path.mkdir(Path(to).parent, exist_ok=True)
    with open(to, "w+") as f:
        f.write(data)


def list_interfaces(interfaces_dir) -> List[str]:
    interfaces = []
    for root, _, files in os.walk(interfaces_dir):
        interfaces.extend(
            [os.path.join(root, file) for file in files if file.endswith(".thrift")]
        )
    return interfaces


def build_output_path(interface, output_dir) -> str:
    return os.path.join(output_dir, Path(interface).name.replace(".thrift", ".pyi"))
