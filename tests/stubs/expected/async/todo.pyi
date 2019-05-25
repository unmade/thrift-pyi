from dataclasses import dataclass
from enum import IntEnum
from typing import *

from . import shared
from . import dates

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
    picture: Optional[str] = None
    is_favorite: bool = False

class Todo:
    async def create(self, text: str, type: int) -> int: ...
    async def update(self, item: TodoItem) -> None: ...
    async def get(self, id: int) -> TodoItem: ...
    async def all(self, pager: shared.LimitOffset) -> List[TodoItem]: ...
    async def filter(self, ids: List[int]) -> List[TodoItem]: ...
    async def stats(self,) -> Dict[int, float]: ...
    async def types(self,) -> Set[int]: ...
    async def groupby(self,) -> Dict[int, List[TodoItem]]: ...
    async def ping(self,) -> str: ...
