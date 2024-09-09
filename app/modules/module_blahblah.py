from d42 import schema
from d42.custom_type import Schema

from app.modules.module import Module
from app.types import (
    AnyTyping,
    CustomTyping,
    DictTyping,
    ListTyping,
    OverloadedFake,
    ScalarTyping,
    SchemaTyping,
    UnknownTypeSchema,
)


class BlahBlahModule(Module):
    def __init__(self):
        super().__init__('blahblah.py')
        self.add_import('typing', 'overload')
        self.overloaded_fakes = []

    def _add_overload(self, method: OverloadedFake):
        if method is not None and method not in self.overloaded_fakes:
            self.overloaded_fakes.append(method)

    def get_ast_content(self) -> list | None:
        imports = [import_.to_ast() for import_ in self.imports]
        methods = [fake.ast_method for fake in self.overloaded_fakes]
        if methods:
            return imports + methods
        return None

    def generate_standard_types(self):
        standard_schemas = [
            (schema.list, ListTyping),
            (schema.bool, ScalarTyping),
            (schema.str, ScalarTyping),
            (schema.int, ScalarTyping),
            (schema.any, AnyTyping),
            (schema.dict, DictTyping),
            (schema.float, ScalarTyping),
            (schema.none, ScalarTyping),
        ]

        for schema_, class_typing in standard_schemas:
            overload, imports = class_typing(schema_.__class__.__name__,
                                             schema_).generate_fake_overload('')
            self.add_import_new(*imports)
            self._add_overload(overload)

        overload, imports = SchemaTyping(Schema).generate_fake_overload()
        self.add_import_new(*imports)
        self._add_overload(overload)

    def generate(self, file_name, schema_name, schema_value):
        if not isinstance(schema_value, Schema):
            return

        if schema_name.startswith('_'):
            return

        schema_for_typing = UnknownTypeSchema(schema_name, schema_value)

        schema_typings = [
            CustomTyping,
            ScalarTyping,
            DictTyping,
            AnyTyping,
            ListTyping,
        ]

        for typing_ in schema_typings:
            if typing_.is_valid_type_for_schema(schema_for_typing):
                overload, imports = typing_(schema_name, schema_value).generate_fake_overload(file_name)
                self.add_import_new(*imports)
                self._add_overload(overload)
