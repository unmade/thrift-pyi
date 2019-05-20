namespace * todo

include "shared.thrift"


enum TodoType {
    PLAIN = 1,
    NOTE = 2,
    CHECKBOXES = 3,
}


struct TodoItem {
    1: required i32 id
    2: required string text
    3: required TodoType type
}

typedef list<TodoItem> TodoItemList


service Todo extends shared.Service {
    void create(
        1: string text,
        2: TodoType type,
    )

    TodoItem get(
        1: i32 id,
    )

    TodoItemList all(

    )

    TodoItemList filter(
        1: list<i32> ids
    )

    map<i32, i64> stats(

    )

    set<i16> types(

    )
}
