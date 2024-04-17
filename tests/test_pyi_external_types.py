import app.modules as modules
from app.helpers import load_module_from_string

"""
Не покрыт:
 - unordered
 - uuid
"""


def test_external_types_pyi():
    code = ("from district42_exp_types.numeric import schema_numeric\n\n\n"
            "TestSchema =  schema_numeric.min(1)")
    module = load_module_from_string('test_scalar', code)

    schema_name = 'TestSchema'
    schema_description = getattr(module, schema_name)

    typed_module = modules.TypedModule('file_name')
    typed_module.generate(schema_name, schema_description)

    assert typed_module.get_printable_content() == (
        'from district42_exp_types.numeric import NumericSchema\n'
        'TestSchema: NumericSchema'
    )


def test_external_types_pyi_blahblah():
    code = ("from district42_exp_types.numeric import schema_numeric\n\n\n"
            "TestSchema =  schema_numeric.min(1)")
    module = load_module_from_string('test_scalar', code)

    schema_name = 'TestSchema'
    schema_description = getattr(module, schema_name)

    blahblah_module = modules.BlahBlahModule()
    blahblah_module.generate('test_file_name', schema_name, schema_description)

    assert blahblah_module.get_printable_content() == (
        'from typing import overload\n'
        'from district42_exp_types.numeric import NumericSchema\n\n'
        '@overload\n'
        'def fake(schema: NumericSchema) -> str:\n'
        '    pass'
    )
