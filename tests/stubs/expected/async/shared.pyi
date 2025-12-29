from dataclasses import dataclass
from typing import *
from . import _typedefs

class NotFound(Exception):
    message: Optional[_typedefs.String] = "Not Found"

    def __init__(self, message: Optional[_typedefs.String] = "Not Found") -> None: ...

class EmptyException(Exception): ...

@dataclass
class LimitOffset:
    limit: Optional[_typedefs.I32] = None
    offset: Optional[_typedefs.I32] = None

INT_CONST_1: int = 1234
MAP_CONST: Dict[str, str] = {"hello": "world", "goodnight": "moon"}
INT_CONST_2: int = 1234
EMPTY_LIST: List[Any] = []
EMPTY_MAP: Dict[Any, Any] = {}
EMPTY_SET: Set[Any] = set()

class Service:
    async def ping(self) -> _typedefs.String: ...
