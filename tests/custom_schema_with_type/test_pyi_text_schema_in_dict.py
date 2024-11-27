import sys

import app.modules as modules
from app.helpers import load_module_from_string
from tests.custom_schema_with_type._text_schema import TEXT_SCHEMA_CODE

SCHEMA_NAME = 'TestSchema'

CODE = '''\
from custom import TextSchema
from d42 import schema

TestSchema = schema.dict({
  'name': TextSchema,
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

BLAHBLAH_PYI = '''\
from typing import overload
from typing import Type
from test.module import TestSchema

@overload
def fake(schema: Type[TestSchema]) -> TestSchema.type:
    pass\
'''


class TestClassTextSchemaInDict:

    def setup_method(self):
        entity_module = load_module_from_string('test_entity', TEXT_SCHEMA_CODE)
        sys.modules['custom'] = entity_module

    def teardown_method(self):
        sys.modules.pop('custom')

    def test_text_schema_in_dict_pyi(self):
        module = load_module_from_string('test_scalar', CODE)
        schema_value = getattr(module, SCHEMA_NAME)

        typed_module = modules.TypedModule('file_name')
        typed_module.generate(SCHEMA_NAME, schema_value)

        assert typed_module.get_printable_content() == CODE_PYI

    def test_text_schema_in_dict_pyi_blahblah(self):
        module = load_module_from_string('test.module', CODE)
        schema_value = getattr(module, SCHEMA_NAME)

        blahblha_module = modules.BlahBlahModule()
        blahblha_module.generate('test.module', SCHEMA_NAME, schema_value)

        assert blahblha_module.get_printable_content() == BLAHBLAH_PYI
