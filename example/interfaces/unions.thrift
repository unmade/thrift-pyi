namespace * unions

include "dates.thrift"

struct Payload {
    1: required string key
    2: required i32 value
}

union SimpleUnion {
    1: string textValue
    2: i32 intValue
    3: Payload payloadValue
}

struct Envelope {
    1: required string id
    2: required SimpleUnion content
    3: optional SimpleUnion extra
}

union TimestampedValue {
    1: string text
    2: dates.DateTime timestamp
}
