from dataclasses import dataclass
from enum import IntEnum
from typing import *

class NotFound(Exception):
    message: Optional[str]

class Service:
    def ping(self,) -> str: ...
