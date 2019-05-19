from enum import IntEnum
from typing import *

from . import shared

class TodoType(IntEnum):
    PLAIN = 1
    NOTE = 2
    CHECKBOXES = 3

class Todo:
    def create(self, text: str) -> None: ...
    def ping(self,) -> str: ...
