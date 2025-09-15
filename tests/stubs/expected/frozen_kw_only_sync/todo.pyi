from dataclasses import dataclass, field
from enum import IntEnum
from typing import *
from . import _typedefs
from . import dates
from . import shared

class TodoType(IntEnum):
    PLAIN = 1
    NOTE = 2
    CHECKBOXES = 3

@dataclass(frozen=True, kw_only=True)
class TodoItem:
    id: _typedefs.I32
    text: _typedefs.String
    type: TodoType
    created: dates.DateTime
    is_deleted: _typedefs.Bool
    picture: Optional[_typedefs.Binary] = None
    createdWithDefault: dates.DateTime = field(
        default_factory=lambda: dates.DateTime(
            year=1970, month=1, day=1, hour=0, minute=0, second=0, microsecond=0
        )
    )
    is_favorite: _typedefs.Bool = False

@dataclass(frozen=True, kw_only=True)
class TodoCounter:
    todos: Dict[_typedefs.I32, TodoItem] = field(default_factory=dict)
    plain_ids: Set[_typedefs.I32] = field(default_factory=lambda: {1, 2, 3})
    note_ids: List[_typedefs.I32] = field(default_factory=list)
    checkboxes_ids: Set[_typedefs.I32] = field(default_factory=set)

default_created_date: dates.DateTime = dates.DateTime(
    year=2024, month=12, day=25, hour=0, minute=0, second=0, microsecond=0
)

class Todo:
    def create(self, text: _typedefs.String, type: TodoType) -> _typedefs.I32: ...
    def update(self, item: TodoItem) -> None: ...
    def get(self, id: _typedefs.I32) -> TodoItem: ...
    def all(self, pager: shared.LimitOffset) -> List[TodoItem]: ...
    def filter(self, ids: List[_typedefs.I32]) -> List[TodoItem]: ...
    def stats(self) -> Dict[_typedefs.I32, _typedefs.Double]: ...
    def types(self) -> Set[_typedefs.I16]: ...
    def groupby(self) -> Dict[TodoType, List[TodoItem]]: ...
    def ping(self) -> _typedefs.String: ...
