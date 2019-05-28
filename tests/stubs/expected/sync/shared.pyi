from dataclasses import dataclass
from typing import *

class NotFound(Exception):
    message: Optional[str] = "Not Found"

@dataclass
class LimitOffset:
    limit: Optional[int] = None
    offset: Optional[int] = None

class Service:
    def ping(self,) -> str: ...
