from __future__ import annotations

from pathlib import Path
from typing import List, Union


def list_interfaces(interfaces_dir: Union[str, Path]) -> List[Path]:
    return list(Path(interfaces_dir).glob("**/*.thrift"))


def save(data: str, to: Union[str, Path]) -> None:
    Path.mkdir(Path(to).parent, exist_ok=True)
    with open(to, "w+", encoding="utf-8") as f:
        f.write(data)
