from dataclasses import dataclass
from typing import *

@dataclass
class DateTime:
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    microsecond: Optional[int] = None

@dataclass
class Date: ...

EPOCH: DateTime = DateTime(
    year=1970, month=1, day=1, hour=0, minute=0, second=0, microsecond=0
)
