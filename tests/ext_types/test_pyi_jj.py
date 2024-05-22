import app.modules as modules
from app.helpers import load_module_from_string

CODE = '''\
from d42 import schema
from jj_district42 import HistoryItemSchema, schema_history_request

TestHistorySchema = HistoryItemSchema + schema.dict({
    "request": schema_history_request
})
'''

CODE_PYI = '''\
from typing import overload
from typing import Literal
from typing import TypedDict
from typing import Any
from typing import List
from district42.types import DateTimeSchema

class _D42MetaTestHistorySchema(type):

    @overload
    def __getitem__(cls, arg: Literal['request']) -> Any:
        pass

    @overload
    def __getitem__(cls, arg: Literal['response']) -> Any:
        pass

    @overload
    def __getitem__(cls, arg: Literal['tags']) -> List:
        pass

    @overload
    def __getitem__(cls, arg: Literal['created_at']) -> DateTimeSchema:
        pass

    def __mod__(self, other):
        pass

    def __add__(self, other):
        pass

class TestHistorySchema(metaclass=_D42MetaTestHistorySchema):

    class type(TypedDict, total=False):
        request: Any
        response: Any
        tags: List
        created_at: DateTimeSchema.type\
'''

CODE_BLAHBLAH_PYI = '''\
from typing import overload
from typing import Type
from test_file_name import TestHistorySchema

@overload
def fake(schema: Type[TestHistorySchema]) -> TestHistorySchema.type:
    pass\
'''


def test_jj_history_pyi():
    module = load_module_from_string('test', CODE)

    schema_name = 'TestHistorySchema'
    schema_description = getattr(module, schema_name)

    typed_module = modules.TypedModule('file_name')
    typed_module.generate(schema_name, schema_description)

    assert typed_module.get_printable_content() == CODE_PYI


def test_jj_history_pyi_blahblah():
    module = load_module_from_string('test', CODE)

    schema_name = 'TestHistorySchema'
    schema_description = getattr(module, schema_name)

    blahblah_module = modules.BlahBlahModule()
    blahblah_module.generate('test_file_name', schema_name, schema_description)

    assert blahblah_module.get_printable_content() == CODE_BLAHBLAH_PYI
