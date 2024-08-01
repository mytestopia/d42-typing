import ast
import typing
from typing import Any, Tuple

from d42.custom_type import CustomSchema

from app.helpers import get_module_to_import_from
from app.modules.module import Import
from app.types._type import Typing, UnknownTypeSchema
from ast_generate import annotated_assign


class CustomTyping(Typing):

    def __init__(self, name, value):
        super().__init__(name, value)
        self.class_name = self.value.type.__name__

    @classmethod
    def is_valid_type_for_schema(cls, schema_: UnknownTypeSchema) -> bool:
        return issubclass(schema_.value.__class__, CustomSchema)

    def generate_pyi(self) -> Tuple[list[ast.AnnAssign], list[Import]]:
        # для схем без типов
        if (
                hasattr(self.value, 'type') is False
                or self.value.type is typing.Any
        ):
            return [], []
        annotation = annotated_assign(self.name, self.class_name)
        imports = [Import(get_module_to_import_from(self.value.type), self.class_name)]
        return [annotation], imports

