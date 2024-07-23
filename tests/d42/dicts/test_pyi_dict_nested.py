import app.modules as modules
from app.helpers import load_module_from_string

SCHEMA_NAME = 'NestedTestSchema'

CODE = '''\
from d42 import schema

NestedTestSchema = schema.dict({
    'id': schema.int,
    'entity': schema.dict({
        'is_deleted': schema.bool,
        'updated_at': schema.int
    })
})
'''

CODE_PYI = '''\
from typing import overload
from typing import Literal
from typing import TypedDict
from district42.types import IntSchema
from district42.types import BoolSchema

class _D42MetaNestedTestSchema_EntitySchema(type):

    @overload
    def __getitem__(cls, arg: Literal['is_deleted']) -> BoolSchema:
        pass

    @overload
    def __getitem__(cls, arg: Literal['updated_at']) -> IntSchema:
        pass

    def __mod__(self, other):
        pass

    def __add__(self, other):
        pass

class NestedTestSchema_EntitySchema(metaclass=_D42MetaNestedTestSchema_EntitySchema):

    class type(TypedDict, total=False):
        is_deleted: BoolSchema.type
        updated_at: IntSchema.type

class _D42MetaNestedTestSchema(type):

    @overload
    def __getitem__(cls, arg: Literal['id']) -> IntSchema:
        pass

    @overload
    def __getitem__(cls, arg: Literal['entity']) -> NestedTestSchema_EntitySchema:
        pass

    def __mod__(self, other):
        pass

    def __add__(self, other):
        pass

class NestedTestSchema(metaclass=_D42MetaNestedTestSchema):

    class type(TypedDict, total=False):
        id: IntSchema.type
        entity: NestedTestSchema_EntitySchema.type\
'''

CODE_BLAHBLAH_PYI = '''\
from typing import overload
from typing import Type
from test.module import NestedTestSchema

@overload
def fake(schema: Type[NestedTestSchema]) -> NestedTestSchema.type:
    pass\
'''


def test_dict_nested_pyi():
    module = load_module_from_string('test_scalar', CODE)

    schema_value = getattr(module, SCHEMA_NAME)

    typed_module = modules.TypedModule('file_name')
    typed_module.generate(SCHEMA_NAME, schema_value)

    assert typed_module.get_printable_content() == CODE_PYI


def test_dict_nested_pyi_blahblah():
    module = load_module_from_string('test.module', CODE)

    schema_value = getattr(module, SCHEMA_NAME)

    blahblah_module = modules.BlahBlahModule()
    blahblah_module.generate('test.module', SCHEMA_NAME, schema_value)

    assert blahblah_module.get_printable_content() == CODE_BLAHBLAH_PYI
