import app.modules as modules
from app.helpers import load_module_from_string
from tests.custom_schema_without_type._image_schema import IMAGE_SCHEMA_CODE

SCHEMA_NAME = 'ImageSchema'


CODE_PYI = '''\
from district42.types import AnySchema
ImageSchema: AnySchema\
'''

BLAHBLAH_PYI = '''\
from typing import overload
from typing import Any
from test.module import ImageSchema

@overload
def fake(schema: ImageSchema) -> Any:
    pass\
'''


def test_self_image_schema_pyi():
    module = load_module_from_string('test_scalar', IMAGE_SCHEMA_CODE)
    schema_value = getattr(module, SCHEMA_NAME)

    typed_module = modules.TypedModule('file_name')
    typed_module.generate(SCHEMA_NAME, schema_value)

    assert typed_module.get_printable_content() == CODE_PYI


def test_self_image_schema_pyi_blahblah():
    module = load_module_from_string('test.module', IMAGE_SCHEMA_CODE)
    schema_value = getattr(module, SCHEMA_NAME)

    blahblha_module = modules.BlahBlahModule()
    blahblha_module.generate('test.module', SCHEMA_NAME, schema_value)

    assert blahblha_module.get_printable_content() == BLAHBLAH_PYI