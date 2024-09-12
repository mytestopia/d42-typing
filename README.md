[![PyPI](https://img.shields.io/pypi/v/d42-typing.svg?style=flat-square&color=rgb(24,114,110,0.8))](https://pypi.python.org/pypi/d42-typing/)
[![Python Version](https://img.shields.io/pypi/pyversions/d42-typing.svg?style=flat-square&color=rgb(14,90,166,0.8))](https://pypi.python.org/pypi/d42-typing/)

# d42-typing

d42-typing is a Python package designed to enhance type-checking capabilities within the d42 ecosystem. 
This package introduces generated type definitions that make it easier to work with D42 schemas by 
providing a more structured and robust type-checking mechanism.

- [Features](#features)
- [How it works](#how-it-works)
- [Example](#example)
  - [Scalar schema](#scalar-schema)
  - [Dict schema](#dict-schema)
  - [Working type hints for PyCharm](#working-type-hints-for-pycharm)
- [Installation & Usage](#installation--usage)
  - [How to configurate type auto-generation in PyCharm](#how-to-configurate-type-auto-generation-in-pycharm)


## Features

- Type Definitions: Provides comprehensive type definitions for various entities within Device42.
- Improved Type Checking: Enhances code safety and reliability by utilizing Python's type hints.

## How it works
- Generates Python type hints from d42 schemas.
- Creates `.pyi` files for each schema file in a specified folder (or default).
- Provides overloads for the `fake` method from d42 library.



## Example

#### Scalar schema
```python
from d42 import schema

# --- scalar.py
ValueSchema = schema.int | schema.float

# --- scalar.pyi 
from ... import ...

ValueSchema: Union[IntSchema, FloatSchema]

# --- blahblah.pyi
from ... import ...

@overload
def fake(schema: ValueSchema) -> Union[int, float]:
    pass
```
#### Dict schema
```python
# --- dict.py
from d42 import schema

DictSchema = schema.dict({
    'id': schema.int,
    'name': schema.str('default_name') | schema.str('custom_name'),
    'phone': schema.str | schema.none,
})

# --- dict.pyi
from ... import ...

class _D42MetaUserSchema(type):

    @overload
    def __getitem__(cls, arg: Literal['id']) -> IntSchema:
        pass

    @overload
    def __getitem__(cls, arg: Literal['name']) -> StrSchema:
        pass

    @overload
    def __getitem__(cls, arg: Literal['phone']) -> Union[StrSchema, NoneSchema]:
        pass

    def __mod__(self, other):
        pass

    def __add__(self, other):
        pass

class UserSchema(metaclass=_D42MetaUserSchema):

    class type(TypedDict, total=False):
        id: IntSchema.type
        name: StrSchema.type
        phone: Union[StrSchema.type, NoneSchema.type]

# --- blahblah.pyi
from typing import overload
from typing import Type
from _tests.schemas.test import UserSchema

@overload
def fake(schema: Type[UserSchema]) -> UserSchema.type:
    pass

```

#### Working type hints for PyCharm

<img src="assets/type_hints.png" alt="drawing" width="400"/>

## Installation & Usage

To install `d42-typing`, use the following command:

```sh
pip install d42-typing
```

To generate type hints, run the following command:

```sh
d42-typing --path-to-schemas scenarios/schemas -a -v
# d42-typing --help
```

### How to configurate type auto-generation in PyCharm

1. Set FileWatcher in PyCharm for auto-generating stubs

   - Go to Pycharm → Settings → Tools → File Watchers 
   - Set the scope pattern: `file[project]:packages/e2e/schemas/*.py`

   <img src="assets/file_watcher_1.png" alt="drawing" width="400"/> <img src="assets/file_watcher_2.png" alt="drawing" width="400"/>

2. Hide .pyi files (if needed): 

   Go to Settings → Editor → File Types → Ignored Files and Folders tab