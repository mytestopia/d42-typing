import app.modules as modules

FAKE_PYI_STANDARD_TYPES = """\
from typing import overload
from typing import List
from d42.declaration.types import ListSchema
from d42.declaration.types import BoolSchema
from d42.declaration.types import StrSchema
from d42.declaration.types import IntSchema
from typing import Any
from d42.declaration.types import AnySchema
from typing import Dict
from d42.declaration.types import DictSchema
from d42.declaration.types import FloatSchema
from d42.declaration.types import NoneSchema
from d42.declaration.types import Schema

@overload
def fake(schema: ListSchema) -> List:
    pass

@overload
def fake(schema: BoolSchema) -> bool:
    pass

@overload
def fake(schema: StrSchema) -> str:
    pass

@overload
def fake(schema: IntSchema) -> int:
    pass

@overload
def fake(schema: AnySchema) -> Any:
    pass

@overload
def fake(schema: DictSchema) -> Dict:
    pass

@overload
def fake(schema: FloatSchema) -> float:
    pass

@overload
def fake(schema: NoneSchema) -> None:
    pass

@overload
def fake(schema: Schema) -> Any:
    pass\
"""


def test_all_mode_pyi_blahblah():

    blahblah_module = modules.FakeModule()
    blahblah_module.generate_standard_types()

    # todo проверять иначе
    assert blahblah_module.get_printable_content() == FAKE_PYI_STANDARD_TYPES
