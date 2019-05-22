namespace * todo

include "shared.thrift"
include "dates.thrift"


enum TodoType {
    PLAIN = 1,
    NOTE = 2,
    CHECKBOXES = 3,
}


struct TodoItem {
    1: required i32 id
    2: required string text
    3: required TodoType type
    4: required dates.DateTime created
    5: required bool is_deleted
    6: optional binary picture
}

typedef list<TodoItem> TodoItemList


service Todo extends shared.Service {
    i32 create(
        1: string text,
        2: TodoType type,
    )

    void update(
        1: i32 id,
        2: string text,
        3: TodoType type,
    )

    TodoItem get(
        1: i32 id,
    ) throws (
        1: shared.NotFound not_found,
    )

    TodoItemList all(
        1: shared.LimitOffset pager
    )

    TodoItemList filter(
        1: list<i32> ids
    )

    map<i32, double> stats(

    )

    set<i16> types(

    )

    map<TodoType, TodoItemList> groupby(

    )
}
