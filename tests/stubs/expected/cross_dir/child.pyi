from dataclasses import dataclass
from enum import IntEnum
from . import _typedefs

class Status(IntEnum):
    ACTIVE = 1
    INACTIVE = 2

@dataclass
class Identifier:
    value: _typedefs.String
    type_id: _typedefs.I32

DEFAULT_ID: Identifier = Identifier(value="unknown", type_id=0)
