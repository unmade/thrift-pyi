from dataclasses import dataclass
from . import _typedefs

@dataclass
class Identifier:
    value: _typedefs.String
    type_id: _typedefs.I32
