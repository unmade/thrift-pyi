from dataclasses import dataclass
from typing import *
from . import _typedefs
from . import child

@dataclass
class ParentRecord:
    name: _typedefs.String
    identifier: child.Identifier
    all_ids: Set[child.Identifier]
