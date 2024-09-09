import app.modules as modules
from app.helpers import load_module_from_string

SCHEMA_NAME = 'TestSchema'

CODE = '''\
from d42 import schema

TestSchema = schema.dict({
    "name": schema.str('a') | schema.str('b')
})
'''

CODE_PYI = '''\
from typing import overload
from typing import Literal
from typing import TypedDict
from district42.types import StrSchema

class _D42MetaTestSchema(type):

    def __getitem__(cls, arg: Literal['name']) -> StrSchema:
        pass

    def __mod__(self, other):
        pass

    def __add__(self, other):
        pass

class TestSchema(metaclass=_D42MetaTestSchema):

    class type(TypedDict, total=False):
        name: StrSchema.type\
'''

CODE_BLAHBLAH_PYI = '''\
from typing import overload
from typing import Type
from test.module import TestSchema

@overload
def fake(schema: Type[TestSchema]) -> TestSchema.type:
    pass\
'''


def test_dict_key_any_same_type_pyi():
    module = load_module_from_string('test', CODE)
    schema_value = getattr(module, SCHEMA_NAME)

    typed_module = modules.TypedModule('file_name')
    typed_module.generate(SCHEMA_NAME, schema_value)

    assert typed_module.get_printable_content() == CODE_PYI


def test_dict_key_any_same_type_pyi_blahblah():
    module = load_module_from_string('test.module', CODE)
    schema_value = getattr(module, SCHEMA_NAME)

    blahblha_module = modules.BlahBlahModule()
    blahblha_module.generate('test.module', SCHEMA_NAME, schema_value)

    assert blahblha_module.get_printable_content() == CODE_BLAHBLAH_PYI
