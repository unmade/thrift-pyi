from __future__ import annotations
from dataclasses import dataclass
from typing import *
from . import _typedefs

@dataclass(frozen=True)
class DateTime:
    year: Optional[_typedefs.I16] = None
    month: Optional[_typedefs.Byte] = None
    day: Optional[_typedefs.Byte] = None
    hour: Optional[_typedefs.I16] = None
    minute: Optional[_typedefs.Byte] = None
    second: Optional[_typedefs.Byte] = None
    microsecond: Optional[_typedefs.I64] = None

@dataclass(frozen=True)
class Date: ...

EPOCH: DateTime = DateTime(
    year=1970, month=1, day=1, hour=0, minute=0, second=0, microsecond=0
)
