from pathlib import Path
from types import ModuleType
from typing import Dict

import thriftpy2

_interfaces_path = Path("example/interfaces")
_interfaces: Dict[str, ModuleType] = {}


def __getattr__(name):
    try:
        return _interfaces[name]
    except KeyError:
        _interfaces[name] = thriftpy2.load(
            str(_interfaces_path.joinpath(f"{name}.thrift"))
        )
        return _interfaces[name]
