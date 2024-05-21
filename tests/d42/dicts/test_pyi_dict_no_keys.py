import app.modules as modules
from app.helpers import load_module_from_string

CODE = '''\
from d42 import schema
TestSchema = schema.dict\
'''

CODE_PYI = '''\
from district42.types import DictSchema
TestSchema: DictSchema\
'''

CODE_BLAHBLAH = '''\
from typing import overload
from typing import Dict
from district42.types import DictSchema

@overload
def fake(schema: DictSchema) -> Dict:
    pass\
'''


def test_dict_pyi_no_keys():
    module = load_module_from_string('test_scalar', CODE)

    schema_name = 'TestSchema'
    schema_description = getattr(module, schema_name)

    typed_module = modules.TypedModule('file_name')
    typed_module.generate(schema_name, schema_description)

    assert typed_module.get_printable_content() == CODE_PYI


def test_dict_pyi_no_keys_blahblah():
    module = load_module_from_string('test.module', CODE)

    schema_name = 'TestSchema'
    schema_description = getattr(module, schema_name)

    blahblha_module = modules.BlahBlahModule()
    blahblha_module.generate('test.module', schema_name, schema_description)

    assert blahblha_module.get_printable_content() == CODE_BLAHBLAH
