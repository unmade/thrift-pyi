namespace * todo

include "shared.thrift"


service Todo extends shared.Service {
    void create(
        1: string text,
    )
}
