import app.modules as modules
from app.helpers import load_module_from_string

"""
Не покрыт:
 - unordered
 - uuid
"""

CODE = '''
from district42_exp_types.numeric import schema_numeric
TestNumericSchema =  schema_numeric.min(1)
'''

CODE_PYI = '''\
from district42_exp_types.numeric import NumericSchema
TestNumericSchema: NumericSchema\
'''

CODE_BLAHBLAH_PYI = '''\
from typing import overload
from district42_exp_types.numeric import NumericSchema

@overload
def fake(schema: NumericSchema) -> str:
    pass\
'''


def test_numeric_pyi():
    module = load_module_from_string('test', CODE)

    schema_name = 'TestNumericSchema'
    schema_description = getattr(module, schema_name)

    typed_module = modules.TypedModule('file_name')
    typed_module.generate(schema_name, schema_description)

    assert typed_module.get_printable_content() == CODE_PYI


def test_numeric_pyi_blahblah():
    module = load_module_from_string('test', CODE)

    schema_name = 'TestNumericSchema'
    schema_description = getattr(module, schema_name)

    blahblah_module = modules.BlahBlahModule()
    blahblah_module.generate('test_file_name', schema_name, schema_description)

    assert blahblah_module.get_printable_content() == CODE_BLAHBLAH_PYI
