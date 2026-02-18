enum Status {
    ACTIVE = 1,
    INACTIVE = 2,
}

struct Identifier {
    1: required string value
    2: required i32 type_id
}

const Identifier DEFAULT_ID = {"value": "unknown", "type_id": 0}
