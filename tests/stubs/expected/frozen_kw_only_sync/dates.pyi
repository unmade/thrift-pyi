from dataclasses import dataclass
from typing import *
from . import _typedefs

@dataclass(frozen=True, kw_only=True)
class DateTime:
    year: _typedefs.I16
    month: _typedefs.Byte
    day: _typedefs.Byte
    hour: _typedefs.I16
    minute: _typedefs.Byte
    second: _typedefs.Byte
    microsecond: Optional[_typedefs.I64] = None

@dataclass(frozen=True, kw_only=True)
class Date: ...

EPOCH: DateTime = DateTime(
    year=1970, month=1, day=1, hour=0, minute=0, second=0, microsecond=0
)
