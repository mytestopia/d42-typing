import sys

import app.modules as modules
from app.helpers import load_module_from_string
from tests.custom_schema_with_type._text_schema import TEXT_SCHEMA_CODE

SCHEMA_NAME = 'TestSchema'

CODE = '''\
from custom import TextSchema
from d42 import schema

TestSchema = TextSchema
'''

CODE_PYI = '''\
from district42.types import StrSchema
TestSchema: StrSchema\
'''

BLAHBLAH_PYI = '''\
from typing import overload
from district42.types import StrSchema

@overload
def fake(schema: StrSchema) -> str:
    pass\
'''


class TestClassTextSchema:

    def setup_method(self):
        entity_module = load_module_from_string('test_entity', TEXT_SCHEMA_CODE)
        sys.modules['custom'] = entity_module

    def teardown_method(self):
        sys.modules.pop('custom')

    def test_text_schema_pyi(self):
        module = load_module_from_string('test_scalar', CODE)
        schema_value = getattr(module, SCHEMA_NAME)

        typed_module = modules.TypedModule('file_name')
        typed_module.generate(SCHEMA_NAME, schema_value)

        assert typed_module.get_printable_content() == CODE_PYI

    def test_text_schema_pyi_blahblah(self):
        module = load_module_from_string('test.module', CODE)
        schema_value = getattr(module, SCHEMA_NAME)

        blahblha_module = modules.BlahBlahModule()
        blahblha_module.generate('test.module', SCHEMA_NAME, schema_value)

        assert blahblha_module.get_printable_content() == BLAHBLAH_PYI
