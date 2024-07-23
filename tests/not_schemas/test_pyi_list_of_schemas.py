import app.modules as modules
from app.helpers import load_module_from_string

SCHEMA_NAME = 'TestSchema'

CODE = '''\
from d42 import schema
TestSchema = [schema.str("string")]
'''


CODE_PYI = '''\
TestSchema: list\
'''


def test_list_of_schemas_pyi():
    module = load_module_from_string('test', CODE)
    schema_description = getattr(module, SCHEMA_NAME)

    typed_module = modules.TypedModule('file_name')
    typed_module.generate(SCHEMA_NAME, schema_description)

    assert typed_module.get_printable_content() == CODE_PYI


def test_list_of_schemas_pyi_blahblah():
    module = load_module_from_string('test', CODE)
    schema_description = getattr(module, SCHEMA_NAME)

    blahblah_module = modules.BlahBlahModule()
    blahblah_module.generate('test_file_name', SCHEMA_NAME, schema_description)

    assert blahblah_module.get_printable_content() is None
