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
