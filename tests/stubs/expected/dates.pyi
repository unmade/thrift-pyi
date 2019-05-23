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
class Date:
    pass
