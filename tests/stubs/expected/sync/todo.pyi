from dataclasses import dataclass
from enum import IntEnum
from typing import *
from . import dates
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
    created: dates.DateTime
    is_deleted: bool
    picture: Optional[bytes] = None
    is_favorite: bool = False

class Todo:
    def create(self, text: str, type: int) -> int: ...
    def update(self, item: TodoItem) -> None: ...
    def get(self, id: int) -> TodoItem: ...
    def all(self, pager: shared.LimitOffset) -> List[TodoItem]: ...
    def filter(self, ids: List[int]) -> List[TodoItem]: ...
    def stats(self) -> Dict[int, float]: ...
    def types(self) -> Set[int]: ...
    def groupby(self) -> Dict[int, List[TodoItem]]: ...
    def ping(self) -> str: ...
