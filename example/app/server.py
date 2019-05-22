import datetime
from typing import TYPE_CHECKING, Dict

from example.app import interfaces
from thriftpy2.rpc import make_server

if TYPE_CHECKING:
    from example.app.interfaces.todo import TodoItem

todos: Dict[int, "TodoItem"] = {}


class Dispatcher(object):
    def create(self, text: str, type: int) -> int:
        todo_id = max(todos.keys() or [0]) + 1
        created = datetime.datetime.now()
        todos[todo_id] = interfaces.todo.TodoItem(
            id=todo_id,
            text=text,
            type=type,
            created=interfaces.dates.DateTime(
                year=created.year,
                month=created.month,
                day=created.day,
                hour=created.hour,
                minute=created.minute,
                second=created.second,
                microsecond=created.microsecond,
            ),
            is_deleted=False,
            picture=None,
        )
        return todo_id

    def get(self, id: int) -> "TodoItem":
        try:
            return todos[id]
        except KeyError:
            raise interfaces.shared.NotFound

    def ping(self):
        return "pong"


if __name__ == "__main__":
    server = make_server(interfaces.todo.Todo, Dispatcher(), "127.0.0.1", 6000)
    server.serve()
