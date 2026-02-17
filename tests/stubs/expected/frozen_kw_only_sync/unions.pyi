from dataclasses import dataclass
from typing import *
from . import _typedefs
from . import dates

@dataclass(frozen=True, kw_only=True)
class Payload:
    key: _typedefs.String
    value: _typedefs.I32

@dataclass(frozen=True, kw_only=True)
class SimpleUnion:
    textValue: Optional[_typedefs.String] = None
    intValue: Optional[_typedefs.I32] = None
    payloadValue: Optional[Payload] = None

@dataclass(frozen=True, kw_only=True)
class Envelope:
    id: _typedefs.String
    content: SimpleUnion
    extra: Optional[SimpleUnion] = None

@dataclass(frozen=True, kw_only=True)
class TimestampedValue:
    text: Optional[_typedefs.String] = None
    timestamp: Optional[dates.DateTime] = None
