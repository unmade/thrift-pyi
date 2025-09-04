from dataclasses import dataclass
from typing import Annotated

@dataclass(frozen=True)
class Metadata:
    thrift_type: str

Binary = Annotated[bytes, Metadata(thrift_type="BINARY")]
Bool = Annotated[bool, Metadata(thrift_type="BOOL")]
Byte = Annotated[int, Metadata(thrift_type="BYTE")]
Double = Annotated[float, Metadata(thrift_type="DOUBLE")]
I16 = Annotated[int, Metadata(thrift_type="I16")]
I32 = Annotated[int, Metadata(thrift_type="I32")]
I64 = Annotated[int, Metadata(thrift_type="I64")]
String = Annotated[str, Metadata(thrift_type="STRING")]
