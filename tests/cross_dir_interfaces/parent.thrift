include "sub/child.thrift"

struct ParentRecord {
    1: required string name
    2: required child.Identifier identifier
    3: required set<child.Identifier> all_ids
    4: required child.Status status
    5: required child.Identifier default_id = child.DEFAULT_ID
}
