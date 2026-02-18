from dataclasses import dataclass
from typing import *
from . import _typedefs

@dataclass(frozen=True)
class Identifier:
    value: Optional[_typedefs.String] = None
    type_id: Optional[_typedefs.I32] = None
