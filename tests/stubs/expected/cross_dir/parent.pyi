from dataclasses import dataclass, field
from typing import *
from . import _typedefs
from . import child

@dataclass
class ParentRecord:
    name: _typedefs.String
    identifier: child.Identifier
    all_ids: Set[child.Identifier]
    status: child.Status
    default_id: child.Identifier = field(
        default_factory=lambda: child.Identifier(value="unknown", type_id=0)
    )
