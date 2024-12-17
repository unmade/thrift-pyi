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

class Todo:
    async def create(self, text: str, type: TodoType) -> int: ...
    async def update(self, item: TodoItem) -> None: ...
    async def get(self, id: int) -> TodoItem: ...
    async def all(self, pager: shared.LimitOffset) -> List[TodoItem]: ...
    async def filter(self, ids: List[int]) -> List[TodoItem]: ...
    async def stats(self) -> Dict[int, float]: ...
    async def types(self) -> Set[int]: ...
    async def groupby(self) -> Dict[TodoType, List[TodoItem]]: ...
    async def ping(self) -> str: ...
