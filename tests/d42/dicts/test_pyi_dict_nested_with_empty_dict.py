import app.modules as modules
from app.helpers import load_module_from_string

SCHEMA_NAME = 'NestedTestSchema'

CODE = '''\
from d42 import schema

NestedTestSchema = schema.dict({
    'data': schema.dict({})
})
'''

CODE_PYI = '''\
from typing import overload
from typing import Literal
from typing import TypedDict
from typing import Dict

class _D42MetaNestedTestSchema(type):

    def __getitem__(cls, arg: Literal['data']) -> Dict:
        pass

    def __mod__(self, other):
        pass

    def __add__(self, other):
        pass

class NestedTestSchema(metaclass=_D42MetaNestedTestSchema):

    class type(TypedDict, total=False):
        data: Dict\
'''

CODE_BLAHBLAH_PYI = '''\
from typing import overload
from typing import Type
from test.module import NestedTestSchema

@overload
def fake(schema: Type[NestedTestSchema]) -> NestedTestSchema.type:
    pass\
'''


def test_dict_nested_empty_dict_key_pyi():
    module = load_module_from_string('test_scalar', CODE)

    schema_value = getattr(module, SCHEMA_NAME)

    typed_module = modules.TypedModule('file_name')
    typed_module.generate(SCHEMA_NAME, schema_value)

    assert typed_module.get_printable_content() == CODE_PYI


def test_dict_nested_empty_dict_key_pyi_blahblah():
    module = load_module_from_string('test.module', CODE)

    schema_value = getattr(module, SCHEMA_NAME)

    blahblah_module = modules.BlahBlahModule()
    blahblah_module.generate('test.module', SCHEMA_NAME, schema_value)

    assert blahblah_module.get_printable_content() == CODE_BLAHBLAH_PYI
