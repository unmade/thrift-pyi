from dataclasses import dataclass
from typing import *
from . import _typedefs
from . import child

@dataclass(kw_only=True)
class ParentRecord:
    name: Optional[_typedefs.String] = None
    identifier: Optional[child.Identifier] = None
    all_ids: Optional[Set[child.Identifier]] = None
