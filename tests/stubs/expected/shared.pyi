from dataclasses import dataclass
from enum import IntEnum
from typing import *

class NotFound(Exception):
    message: Optional[str]

@dataclass
class LimitOffset:
    limit: int
    offset: int

class Service:
    def ping(self,) -> str: ...
