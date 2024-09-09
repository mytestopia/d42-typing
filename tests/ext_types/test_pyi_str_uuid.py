import app.modules as modules
from app.helpers import load_module_from_string

CODE = '''\
from district42_exp_types.uuid_str import schema_uuid_str
StrUuidExampleSchema = schema_uuid_str
'''

CODE_PYI = '''\
from district42_exp_types.uuid_str import UUIDStrSchema
StrUuidExampleSchema: UUIDStrSchema\
'''

CODE_BLAHBLAH_PYI = '''\
from typing import overload
from district42_exp_types.uuid_str import UUIDStrSchema
from typing import Any

@overload
def fake(schema: UUIDStrSchema) -> Any:
    pass\
'''


def test_str_uuid_pyi():
    module = load_module_from_string('test', CODE)

    schema_name = 'StrUuidExampleSchema'
    schema_description = getattr(module, schema_name)

    typed_module = modules.TypedModule('file_name')
    typed_module.generate(schema_name, schema_description)

    assert typed_module.get_printable_content() == CODE_PYI


def test_str_uuid_pyi_blahblah():
    module = load_module_from_string('test', CODE)

    schema_name = 'StrUuidExampleSchema'
    schema_description = getattr(module, schema_name)

    blahblah_module = modules.BlahBlahModule()
    blahblah_module.generate('test_file_name', schema_name, schema_description)

    assert blahblah_module.get_printable_content() == CODE_BLAHBLAH_PYI
