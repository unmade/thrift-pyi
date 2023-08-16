exception NotFound {
    1: optional string message = "Not Found"
}

exception EmptyException {}

const i32 INT_CONST_1 = 1234
const map<string,string> MAP_CONST = {"hello": "world", "goodnight": "moon"}
const i32 INT_CONST_2 = 1234

struct LimitOffset {
    1: optional i32 limit
    2: optional i32 offset
}


service Service {
    string ping();
}
