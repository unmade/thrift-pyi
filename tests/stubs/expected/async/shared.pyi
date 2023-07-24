from dataclasses import dataclass
from typing import *

class NotFound(Exception):
    message: Optional[str] = "Not Found"

    def __init__(self, message: Optional[str] = "Not Found") -> None: ...

class EmptyException(Exception): ...

@dataclass
class LimitOffset:
    limit: Optional[int] = None
    offset: Optional[int] = None

class Service:
    async def ping(self) -> str: ...
