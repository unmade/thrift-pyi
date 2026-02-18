from dataclasses import dataclass
from . import _typedefs

@dataclass(frozen=True, kw_only=True)
class Identifier:
    value: _typedefs.String
    type_id: _typedefs.I32
