import app.modules as modules
from app.helpers import load_module_from_string

CODE = '''\
from d42 import schema
TestSchema = schema.dict({
    'id': schema.str,
    'from': schema.str
})\
'''

CODE_PYI = '''\
from typing import overload
from typing import Literal
from typing import TypedDict
from district42.types import StrSchema

class _D42MetaTestSchema(type):

    @overload
    def __getitem__(cls, arg: Literal['id']) -> StrSchema:
        pass

    @overload
    def __getitem__(cls, arg: Literal['from']) -> StrSchema:
        pass

    def __mod__(self, other):
        pass

    def __add__(self, other):
        pass

class TestSchema(metaclass=_D42MetaTestSchema):
    type = TypedDict('type', {'id': StrSchema.type, 'from': StrSchema.type}, total=False)\
'''

CODE_BLAHBLAH = '''\
from typing import overload
from typing import Dict
from district42.types import DictSchema

@overload
def fake(schema: DictSchema) -> Dict:
    pass\
'''


def test_dict_key_keyword_pyi():
    module = load_module_from_string('test_scalar', CODE)

    schema_name = 'TestSchema'
    schema_description = getattr(module, schema_name)

    typed_module = modules.TypedModule('file_name')
    typed_module.generate(schema_name, schema_description)

    assert typed_module.get_printable_content() == CODE_PYI


def test_dict_key_keyword_blahblah_pyi():
    module = load_module_from_string('test.module', CODE)

    schema_name = 'TestSchema'
    schema_description = getattr(module, schema_name)

    blahblha_module = modules.BlahBlahModule()
    blahblha_module.generate('test.module', schema_name, schema_description)

    assert blahblha_module.get_printable_content() == CODE_BLAHBLAH
