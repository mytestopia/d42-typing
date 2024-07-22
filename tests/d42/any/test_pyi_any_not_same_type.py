import app.modules as modules
from app.helpers import load_module_from_string

SCHEMA_NAME = 'TestSchema'

CODE = '''\
from d42 import schema
TestSchema = schema.any(schema.str('A'), schema.none)
'''

CODE_PYI = '''\
from typing import Union
from district42.types import StrSchema
from district42.types import NoneSchema
TestSchema: Union[StrSchema, NoneSchema]\
'''

BLAHBLAH_PYI = '''\
from typing import overload
from typing import Union
from test_file_name import TestSchema

@overload
def fake(schema: TestSchema) -> Union[str, None]:
    pass\
'''


def test_any_not_same_type_pyi():
    module = load_module_from_string('test_scalar', CODE)
    schema_description = getattr(module, SCHEMA_NAME)

    typed_module = modules.TypedModule('file_name')
    typed_module.generate(SCHEMA_NAME, schema_description)

    assert typed_module.get_printable_content() == CODE_PYI


def test_any_not_same_type_pyi_blahblah():
    module = load_module_from_string('test_scalar', CODE)
    schema_description = getattr(module, SCHEMA_NAME)

    blahblah_module = modules.BlahBlahModule()
    blahblah_module.generate('test_file_name', SCHEMA_NAME, schema_description)

    assert blahblah_module.get_printable_content() == BLAHBLAH_PYI
