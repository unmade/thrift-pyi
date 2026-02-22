from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from typing import *
from . import _typedefs

class LabelColor(IntEnum):
    RED = 1
    GREEN = 2
    BLUE = 3

@dataclass(frozen=True, kw_only=True)
class Label:
    name: Optional[_typedefs.String] = None
    color: Optional[_typedefs.I32] = None

DEFAULT_LABEL: Label = Label(name="default", color=3)
