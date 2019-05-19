namespace * todo

include "shared.thrift"


enum TodoType {
    PLAIN = 1,
    NOTE = 2,
    CHECKBOXES = 3,
}


service Todo extends shared.Service {
    void create(
        1: string text,
    )
}
