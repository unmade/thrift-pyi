exception NotFound {
    1: optional string message
}


struct LimitOffset {
    1: optional i32 limit
    2: optional i32 offset
}


service Service {
    string ping();
}
