from __future__ import annotations

from pathlib import Path


def list_interfaces(interfaces_dir: str | Path) -> list[Path]:
    return list(Path(interfaces_dir).glob("**/*.thrift"))


def save(data: str, to: str | Path) -> None:
    Path.mkdir(Path(to).parent, exist_ok=True)
    with open(to, "w+", encoding="utf-8") as f:
        f.write(data)
