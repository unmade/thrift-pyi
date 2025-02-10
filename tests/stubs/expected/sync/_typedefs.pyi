from typing import Annotated

Binary = Annotated[bytes, {"thrift_type": "BINARY"}]
Bool = Annotated[bool, {"thrift_type": "BOOL"}]
Byte = Annotated[int, {"thrift_type": "BYTE"}]
Double = Annotated[float, {"thrift_type": "DOUBLE"}]
I16 = Annotated[int, {"thrift_type": "I16"}]
I32 = Annotated[int, {"thrift_type": "I32"}]
I64 = Annotated[int, {"thrift_type": "I64"}]
String = Annotated[str, {"thrift_type": "STRING"}]
