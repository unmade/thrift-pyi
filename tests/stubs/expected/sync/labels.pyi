from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from . import _typedefs

class LabelColor(IntEnum):
    RED = 1
    GREEN = 2
    BLUE = 3

@dataclass
class Label:
    name: _typedefs.String
    color: LabelColor

DEFAULT_LABEL: Label = Label(name="default", color=3)
