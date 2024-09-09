import app.modules as modules
from app.helpers import load_module_from_string

NAME = 'TestUUID4Schema'

CODE = '''\
from d42 import schema
TestUUID4Schema = schema.uuid4
'''

CODE_PYI = '''\
from district42.types import UUID4Schema
TestUUID4Schema: UUID4Schema\
'''

CODE_BLAHBLAH_PYI = '''\
from typing import overload
from district42.types import UUID4Schema
from typing import Any

@overload
def fake(schema: UUID4Schema) -> Any:
    pass\
'''


def test_scalar_uuid4_pyi():
    module = load_module_from_string('test', CODE)
    schema_description = getattr(module, NAME)

    typed_module = modules.TypedModule('file_name')
    typed_module.generate(NAME, schema_description)

    assert typed_module.get_printable_content() == CODE_PYI


def test_scalar_uuid4_pyi_blahblah():
    module = load_module_from_string('test', CODE)
    schema_description = getattr(module, NAME)

    blahblah_module = modules.BlahBlahModule()
    blahblah_module.generate('test_file_name', NAME, schema_description)

    assert blahblah_module.get_printable_content() == CODE_BLAHBLAH_PYI
