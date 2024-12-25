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
    id: int
    text: str
    type: TodoType
    created: dates.DateTime
    is_deleted: bool
    picture: Optional[bytes] = None
    is_favorite: bool = False

@dataclass
class TodoCounter:
    todos: Dict[int, TodoItem] = field(default_factory=dict)
    plain_ids: Set[int] = field(default_factory=lambda: {1, 2, 3})
    note_ids: List[int] = field(default_factory=list)
    checkboxes_ids: Set[int] = field(default_factory=set)

default_created_date: dates.DateTime = dates.DateTime(
    year=2024, month=12, day=25, hour=0, minute=0, second=0, microsecond=0
)

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
