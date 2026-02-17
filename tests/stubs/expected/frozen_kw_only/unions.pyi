from dataclasses import dataclass
from typing import *
from . import _typedefs
from . import dates

@dataclass(frozen=True, kw_only=True)
class Payload:
    key: Optional[_typedefs.String] = None
    value: Optional[_typedefs.I32] = None

@dataclass(frozen=True, kw_only=True)
class SimpleUnion:
    textValue: Optional[_typedefs.String] = None
    intValue: Optional[_typedefs.I32] = None
    payloadValue: Optional[Payload] = None

@dataclass(frozen=True, kw_only=True)
class Envelope:
    id: Optional[_typedefs.String] = None
    content: Optional[SimpleUnion] = None
    extra: Optional[SimpleUnion] = None

@dataclass(frozen=True, kw_only=True)
class TimestampedValue:
    text: Optional[_typedefs.String] = None
    timestamp: Optional[dates.DateTime] = None
