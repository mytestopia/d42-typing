import app.modules as modules
from app.helpers import load_module_from_string
from tests.custom_schema_without_type._image_schema import IMAGE_SCHEMA_CODE

SCHEMA_NAME = 'ImageSchema'

FAKE_PYI = '''\
from typing import overload
from typing import Any
from test.module import _ImageSchema

@overload
def fake(schema: _ImageSchema) -> Any:
    pass\
'''


def test_self_image_schema_pyi():
    module = load_module_from_string('test_scalar', IMAGE_SCHEMA_CODE)
    schema_value = getattr(module, SCHEMA_NAME)

    typed_module = modules.TypedSchemaModule('file_name')
    typed_module.generate(SCHEMA_NAME, schema_value)

    assert typed_module.get_printable_content() is None


def test_self_image_schema_pyi_blahblah():
    module = load_module_from_string('test.module', IMAGE_SCHEMA_CODE)
    schema_value = getattr(module, SCHEMA_NAME)

    blahblha_module = modules.FakeModule()
    blahblha_module.generate('test.module', SCHEMA_NAME, schema_value)

    assert blahblha_module.get_printable_content() == FAKE_PYI
