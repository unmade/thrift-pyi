from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from typing import *
from . import _typedefs

class LabelColor(IntEnum):
    RED = 1
    GREEN = 2
    BLUE = 3

@dataclass
class Label:
    name: Optional[_typedefs.String] = None
    color: Optional[LabelColor] = None

DEFAULT_LABEL: Label = Label(name="default", color=3)
