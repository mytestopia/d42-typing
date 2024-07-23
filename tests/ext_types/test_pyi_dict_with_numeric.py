import app.modules as modules
from app.helpers import load_module_from_string

SCHEMA_NAME = 'TestDictNumericSchema'

CODE = '''\
from d42 import schema
from district42_exp_types.numeric import schema_numeric

TestDictNumericSchema = schema.dict({
    "id": schema_numeric.min(1),
    "first_name": schema.str,
})
'''

CODE_PYI = '''\
from typing import overload
from typing import Literal
from typing import TypedDict
from district42_exp_types.numeric import NumericSchema
from district42.types import StrSchema

class _D42MetaTestDictNumericSchema(type):

    @overload
    def __getitem__(cls, arg: Literal['id']) -> NumericSchema:
        pass

    @overload
    def __getitem__(cls, arg: Literal['first_name']) -> StrSchema:
        pass

    def __mod__(self, other):
        pass

    def __add__(self, other):
        pass

class TestDictNumericSchema(metaclass=_D42MetaTestDictNumericSchema):

    class type(TypedDict, total=False):
        id: NumericSchema.type
        first_name: StrSchema.type\
'''

CODE_BLAHBLAH_PYI = '''\
from typing import overload
from typing import Type
from test.module import TestDictNumericSchema

@overload
def fake(schema: Type[TestDictNumericSchema]) -> TestDictNumericSchema.type:
    pass\
'''


def test_dict_numeric_pyi():
    module = load_module_from_string('test', CODE)
    schema_value = getattr(module, SCHEMA_NAME)

    typed_module = modules.TypedModule('file_name')
    typed_module.generate(SCHEMA_NAME, schema_value)

    assert typed_module.get_printable_content() == CODE_PYI


def test_dict_numeric_pyi_blahblah():
    module = load_module_from_string('test.module', CODE)
    schema_value = getattr(module, SCHEMA_NAME)

    blahblha_module = modules.BlahBlahModule()
    blahblha_module.generate('test.module', SCHEMA_NAME, schema_value)

    assert blahblha_module.get_printable_content() == CODE_BLAHBLAH_PYI
