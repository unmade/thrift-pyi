exception NotFound {
    1: optional string message = "Not Found"
}

exception EmptyException {}

const i32 INT_CONST_1 = 1234
const map<string,string> MAP_CONST = {"hello": "world", "goodnight": "moon"}
const i32 INT_CONST_2 = 1234
const list<string> EMPTY_LIST = []
const map<string,i32> EMPTY_MAP = {}
const set<i32> EMPTY_SET = []

struct LimitOffset {
    1: optional i32 limit
    2: optional i32 offset
}


service Service {
    string ping();
}
