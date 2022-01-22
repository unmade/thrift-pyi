from dataclasses import dataclass
from typing import *

class NotFound(Exception):
    def __init__(self, message: Optional[str] = "Not Found",): ...

class EmptyException(Exception):
    pass

@dataclass
class LimitOffset:
    limit: Optional[int] = None
    offset: Optional[int] = None

class Service:
    def ping(self,) -> str: ...
