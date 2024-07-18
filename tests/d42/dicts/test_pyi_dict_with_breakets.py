import app.modules as modules
from app.helpers import load_module_from_string

SCHEMA_NAME = 'TestSchema'

CODE = '''\
from d42 import schema

TestSchema = schema.dict({
    "id": schema.int,
    "name[first]": schema.str,
})
'''

CODE_PYI = '''\
from district42.types import DictSchema
TestSchema: DictSchema\
'''

CODE_BLAHBLAH_PYI = '''\
from typing import overload
from typing import Dict
from district42.types import DictSchema

@overload
def fake(schema: DictSchema) -> Dict:
    pass\
'''


def test_dict_with_breakets_pyi():
    module = load_module_from_string('test', CODE)
    schema_value = getattr(module, SCHEMA_NAME)

    typed_module = modules.TypedModule('file_name')
    typed_module.generate(SCHEMA_NAME, schema_value)

    assert typed_module.get_printable_content() == CODE_PYI


def test_dict_with_breakets_pyi_blahblah():
    module = load_module_from_string('test.module', CODE)
    schema_value = getattr(module, SCHEMA_NAME)

    blahblha_module = modules.BlahBlahModule()
    blahblha_module.generate('test.module', SCHEMA_NAME, schema_value)

    assert blahblha_module.get_printable_content() == CODE_BLAHBLAH_PYI
