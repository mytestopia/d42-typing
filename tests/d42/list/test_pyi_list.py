import app.modules as modules
from app.helpers import load_module_from_string

SCHEMA_NAME = 'TestSchema'

CODE = '''\
from d42 import schema
TestSchema = schema.list
'''

CODE_PYI = '''\
from district42.types import ListSchema
TestSchema: ListSchema\
'''

BLAHBLAH_PYI = '''\
from typing import overload
from typing import List
from district42.types import ListSchema

@overload
def fake(schema: ListSchema) -> List:
    pass\
'''


def test_list_pyi():
    module = load_module_from_string('test', CODE)
    schema_description = getattr(module, SCHEMA_NAME)

    typed_module = modules.TypedModule('file_name')
    typed_module.generate(SCHEMA_NAME, schema_description)

    assert typed_module.get_printable_content() == CODE_PYI


def test_scalar_pyi_list_blahblah():
    module = load_module_from_string('test_scalar', CODE)
    schema_description = getattr(module, SCHEMA_NAME)

    blahblah_module = modules.BlahBlahModule()
    blahblah_module.generate('test_file_name', SCHEMA_NAME, schema_description)

    assert blahblah_module.get_printable_content() == BLAHBLAH_PYI
