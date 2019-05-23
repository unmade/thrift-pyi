from typing import TYPE_CHECKING

from example.app import interfaces
from thriftpy2.rpc import make_client

if TYPE_CHECKING:
    from example.app.interfaces.todo import Todo


if __name__ == "__main__":
    client: "Todo" = make_client(interfaces.todo.Todo, "127.0.0.1", 6000)

    todo_id = client.create(text="item", type=interfaces.todo.TodoType.NOTE)
    print(f"CREATE = {todo_id}")
    print(f"GET    = {client.get(id=todo_id)}")
    try:
        client.get(id=todo_id + 1)
    except interfaces.shared.NotFound:
        print(f"NOT FOUND")
