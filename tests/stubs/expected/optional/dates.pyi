from dataclasses import dataclass
from typing import *

@dataclass
class DateTime:
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None
    hour: Optional[int] = None
    minute: Optional[int] = None
    second: Optional[int] = None
    microsecond: Optional[int] = None

@dataclass
class Date: ...

EPOCH: DateTime = DateTime(
    year=1970, month=1, day=1, hour=0, minute=0, second=0, microsecond=0
)
