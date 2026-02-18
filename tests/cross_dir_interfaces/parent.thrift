include "sub/child.thrift"

struct ParentRecord {
    1: required string name
    2: required child.Identifier identifier
    3: required set<child.Identifier> all_ids
}
