from dataclasses import dataclass
from enum import IntEnum
from typing import *

class NotFound(Exception):
    message: Optional[str]

@dataclass
class LimitOffset:
    limit: Optional[int]
    offset: Optional[int]

class Service:
    def ping(self,) -> str: ...
