import app.modules as modules

BLAHBLAH_PYI_STANDARD_TYPES = """\
from typing import overload
from typing import List
from district42.types import ListSchema
from district42.types import BoolSchema
from district42.types import StrSchema
from district42.types import IntSchema
from typing import Any
from district42.types import AnySchema
from typing import Dict
from district42.types import DictSchema
from district42.types import FloatSchema
from district42.types import NoneSchema
from district42.types import Schema

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

    blahblah_module = modules.BlahBlahModule()
    blahblah_module.generate_standard_types()

    # todo проверять иначе
    assert blahblah_module.get_printable_content() == BLAHBLAH_PYI_STANDARD_TYPES
