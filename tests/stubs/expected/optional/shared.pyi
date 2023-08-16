from dataclasses import dataclass
from typing import *

INT_CONST_1: int = 1234
MAP_CONST: Dict[str, str] = {"hello": "world", "goodnight": "moon"}
INT_CONST_2: int = 1234

class NotFound(Exception):
    message: Optional[str] = "Not Found"

    def __init__(self, message: Optional[str] = "Not Found") -> None: ...

class EmptyException(Exception): ...

@dataclass
class LimitOffset:
    limit: Optional[int] = None
    offset: Optional[int] = None

class Service:
    def ping(self) -> str: ...
