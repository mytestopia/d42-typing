import app.modules as modules
from app.helpers import load_module_from_string

SCHEMA_NAME = 'TestSchema'

CODE = '''\
from d42 import schema

TestSchema = schema.dict({
    "id": schema.any,
})
'''

CODE_PYI = '''\
from typing import overload
from typing import Literal
from typing import TypedDict
from d42.declaration.types import AnySchema

class _D42MetaTestSchema(type):

    def __getitem__(cls, arg: Literal['id']) -> AnySchema:
        pass

    def __mod__(self, other):
        pass

    def __add__(self, other):
        pass

class TestSchema(metaclass=_D42MetaTestSchema):

    class type(TypedDict, total=False):
        id: AnySchema.type\
'''

CODE_BLAHBLAH_PYI = '''\
from typing import overload
from typing import Type
from test.module import TestSchema

@overload
def fake(schema: Type[TestSchema]) -> TestSchema.type:
    pass\
'''


def test_dict_key_any_schema_pyi():
    module = load_module_from_string('test', CODE)
    schema_value = getattr(module, SCHEMA_NAME)

    typed_module = modules.TypedSchemaModule('file_name')
    typed_module.generate(SCHEMA_NAME, schema_value)

    assert typed_module.get_printable_content() == CODE_PYI


def test_dict_key_key_any_schema_pyi_blahblah():
    module = load_module_from_string('test.module', CODE)
    schema_value = getattr(module, SCHEMA_NAME)

    blahblha_module = modules.FakeModule()
    blahblha_module.generate('test.module', SCHEMA_NAME, schema_value)

    assert blahblha_module.get_printable_content() == CODE_BLAHBLAH_PYI
