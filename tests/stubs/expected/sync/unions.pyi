from dataclasses import dataclass
from typing import *
from . import _typedefs
from . import dates

@dataclass
class Payload:
    key: _typedefs.String
    value: _typedefs.I32

@dataclass
class SimpleUnion:
    textValue: Optional[_typedefs.String] = None
    intValue: Optional[_typedefs.I32] = None
    payloadValue: Optional[Payload] = None

@dataclass
class Envelope:
    id: _typedefs.String
    content: SimpleUnion
    extra: Optional[SimpleUnion] = None

@dataclass
class TimestampedValue:
    text: Optional[_typedefs.String] = None
    timestamp: Optional[dates.DateTime] = None
