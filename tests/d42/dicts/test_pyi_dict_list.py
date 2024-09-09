import pytest

import app.modules as modules
from app.helpers import load_module_from_string

SCHEMA_NAME = 'TestSchema'

CODE = '''\
from d42 import schema

TestSchema = schema.dict({
    "ids": schema.list(schema.int),
})
'''

CODE_PYI = '''\
from typing import overload
from typing import Literal
from typing import TypedDict
from district42.types import IntSchema

class _D42MetaTestSchema(type):

    @overload
    def __getitem__(cls, arg: Literal['ids']) -> ListSchema:
        pass

    def __mod__(self, other):
        pass

    def __add__(self, other):
        pass

class TestSchema(metaclass=_D42MetaTestSchema):

    class type(TypedDict, total=False):
        ids: List[SchemaInt.type]\
'''

CODE_BLAHBLAH_PYI = '''\
from typing import overload
from typing import Type
from typing import List
from test.module import TestSchema

@overload
def fake(schema: Type[TestSchema]) -> List[str]:
    pass\
'''


@pytest.mark.skip  # FIXME
def test_dict_with_list_pyi():
    module = load_module_from_string('test', CODE)
    schema_value = getattr(module, SCHEMA_NAME)

    typed_module = modules.TypedModule('file_name')
    typed_module.generate(SCHEMA_NAME, schema_value)

    assert typed_module.get_printable_content() == CODE_PYI


@pytest.mark.skip  # FIXME
def test_dict_with_list_pyi_blahblah():
    module = load_module_from_string('test.module', CODE)
    schema_value = getattr(module, SCHEMA_NAME)

    blahblha_module = modules.BlahBlahModule()
    blahblha_module.generate('test.module', SCHEMA_NAME, schema_value)

    assert blahblha_module.get_printable_content() == CODE_BLAHBLAH_PYI
