import typing

from d42.custom_type import Schema

from app.helpers import is_builtin_class_instance
from app.types import (
    AnyTyping,
    CustomTyping,
    DictTyping,
    ListTyping,
    ScalarTyping,
    UnknownTypeSchema,
)
from ast_generate import annotated_assign

from .module import Module


class TypedModule(Module):

    def _add_typing(self, item):
        self.typed_items.append(item)

    def _add_typings(self, items):
        for item in items:
            self.typed_items.append(item)

    def get_ast_content(self) -> list[str] | None:
        imports = [import_.to_ast() for import_ in self.imports]
        items = self.typed_items
        if items:
            return imports + items
        return None

    def generate(self, schema_name: str, schema_value: typing.Any):
        if not isinstance(schema_value, Schema):
            if is_builtin_class_instance(type(schema_value)):
                self._add_typing(annotated_assign(schema_name, type(schema_value).__name__))
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
                annotations, imports = typing_(schema_name, schema_value).generate_pyi()
                self.add_import_new(*imports)
                self._add_typings(annotations)
                return
