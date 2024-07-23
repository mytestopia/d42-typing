import pytest

import app.modules as modules
from app.helpers import load_module_from_string


@pytest.mark.parametrize('schema, schema_type', [
    ('schema.str', 'StrSchema'),
    ('schema.float', 'FloatSchema'),
    ('schema.bool', 'BoolSchema'),
    ('schema.int', 'IntSchema'),
    ('schema.bytes', 'BytesSchema'),
    ('schema.none', 'NoneSchema'),
    ('schema.datetime', 'DateTimeSchema'),
])
def test_scalar_pyi(schema, schema_type):
    code = """from d42 import schema\n\n\nTestSchema = {}""".format(schema)
    module = load_module_from_string('test_scalar', code)

    schema_name = 'TestSchema'
    schema_description = getattr(module, schema_name)

    typed_module = modules.TypedModule('file_name')
    typed_module.generate(schema_name, schema_description)

    assert typed_module.get_printable_content() == (
        f'from district42.types import {schema_type}\n'
        f'TestSchema: {schema_type}'
    )


@pytest.mark.parametrize('schema, input_type, output_type', [
    ('schema.str', 'StrSchema', 'str'),
    ('schema.float', 'FloatSchema', 'float'),
    ('schema.bool', 'BoolSchema', 'bool'),
    ('schema.int', 'IntSchema', 'int'),
    ('schema.bytes', 'BytesSchema', 'bytes'),
    ('schema.none', 'NoneSchema', 'None'),
    ('schema.datetime', 'DateTimeSchema', 'str'),
])
def test_scalar_pyi_blahblah(schema, input_type, output_type):
    code = """from d42 import schema\n\n\nTestSchema = {}""".format(schema)
    module = load_module_from_string('test_scalar', code)

    schema_name = 'TestSchema'
    schema_description = getattr(module, schema_name)

    blahblah_module = modules.BlahBlahModule()
    blahblah_module.generate('test_file_name', schema_name, schema_description)

    assert blahblah_module.get_printable_content() == (
        f'from typing import overload\n'
        f'from district42.types import {input_type}\n'
        f'\n'
        f'@overload\n'
        f'def fake(schema: {input_type}) -> {output_type}:\n'
        f'    pass'
    )
