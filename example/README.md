# Example app

This example app shows how to use [generated .pyi files](app/interfaces)
in order to have correct autocomplete and type checking for dynamically loaded thrift interfaces

## Overview

Stubs were created with command:

    thriftpyi example/interfaces --output example/app/interfaces

Note, that [\_\_init__.py](app/interfaces/__init__.py) was created by hand and not by the script.
This file is responsible for the actual access to thrift interfaces.

## Consideration

Normally you must do import like this:
```python
from example.app import interfaces
```

Imports like this will no work:
```python
# DANGER!!! THIS WILL NOT WORK
from example.app.interfaces.todo import Todo
```

Although, if you still want do import things like shown above you can do it like this:
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from example.app.interfaces.todo import Todo
```
