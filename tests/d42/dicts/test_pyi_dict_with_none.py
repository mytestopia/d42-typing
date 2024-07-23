import app.modules as modules
from app.helpers import load_module_from_string

SCHEMA_NAME = 'TestDictNoneSchema'

CODE = '''\
from d42 import schema, optional

TestDictNoneSchema = schema.dict({
    "id": schema.int,
    "flag": schema.none,
})
'''

CODE_PYI = '''\
from typing import overload
from typing import Literal
from typing import TypedDict
from district42.types import IntSchema
from district42.types import NoneSchema

class _D42MetaTestDictNoneSchema(type):

    @overload
    def __getitem__(cls, arg: Literal['id']) -> IntSchema:
        pass

    @overload
    def __getitem__(cls, arg: Literal['flag']) -> NoneSchema:
        pass

    def __mod__(self, other):
        pass

    def __add__(self, other):
        pass

class TestDictNoneSchema(metaclass=_D42MetaTestDictNoneSchema):

    class type(TypedDict, total=False):
        id: IntSchema.type
        flag: NoneSchema.type\
'''

CODE_BLAHBLAH_PYI = '''\
from typing import overload
from typing import Type
from test.module import TestDictNoneSchema

@overload
def fake(schema: Type[TestDictNoneSchema]) -> TestDictNoneSchema.type:
    pass\
'''


def test_dict_none_pyi():
    module = load_module_from_string('test', CODE)
    schema_value = getattr(module, SCHEMA_NAME)

    typed_module = modules.TypedModule('file_name')
    typed_module.generate(SCHEMA_NAME, schema_value)

    assert typed_module.get_printable_content() == CODE_PYI


def test_dict_none_pyi_blahblah():
    module = load_module_from_string('test.module', CODE)
    schema_value = getattr(module, SCHEMA_NAME)

    blahblha_module = modules.BlahBlahModule()
    blahblha_module.generate('test.module', SCHEMA_NAME, schema_value)

    assert blahblha_module.get_printable_content() == CODE_BLAHBLAH_PYI
