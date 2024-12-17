from dataclasses import dataclass, field
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
    id: Optional[int] = None
    text: Optional[str] = None
    type: Optional[TodoType] = None
    created: Optional[dates.DateTime] = None
    is_deleted: Optional[bool] = None
    picture: Optional[bytes] = None
    is_favorite: Optional[bool] = False

@dataclass
class TodoCounter:
    todos: Optional[Dict[int, TodoItem]] = field(default_factory=dict)
    plain_ids: Optional[Set[int]] = field(default_factory=lambda: {1, 2, 3})
    note_ids: Optional[List[int]] = field(default_factory=list)
    checkboxes_ids: Optional[Set[int]] = field(default_factory=set)

class Todo:
    def create(self, text: str, type: TodoType) -> int: ...
    def update(self, item: TodoItem) -> None: ...
    def get(self, id: int) -> TodoItem: ...
    def all(self, pager: shared.LimitOffset) -> List[TodoItem]: ...
    def filter(self, ids: List[int]) -> List[TodoItem]: ...
    def stats(self) -> Dict[int, float]: ...
    def types(self) -> Set[int]: ...
    def groupby(self) -> Dict[TodoType, List[TodoItem]]: ...
    def ping(self) -> str: ...
