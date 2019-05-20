from dataclasses import dataclass
from enum import IntEnum
from typing import *

from . import shared

class TodoType(IntEnum):
    PLAIN = 1
    NOTE = 2
    CHECKBOXES = 3

@dataclass
class TodoItem:
    id: int
    text: str
    type: int

class Todo:
    def create(self, text: str, type: int) -> None: ...
    def get(self, id: int) -> TodoItem: ...
    def all(self,) -> List[TodoItem]: ...
    def filter(self, ids: List[int]) -> List[TodoItem]: ...
    def stats(self,) -> Dict[int, int]: ...
    def ping(self,) -> str: ...
