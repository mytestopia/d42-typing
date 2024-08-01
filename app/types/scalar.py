import ast
from typing import Any, Tuple

from app.helpers import get_module_to_import_from
from app.modules.module import Import
from app.types._type import Typing, UnknownTypeSchema
from ast_generate import annotated_assign


class ScalarTyping(Typing):

    @classmethod
    def is_valid_type_for_schema(cls, schema_: UnknownTypeSchema) -> bool:
        scalar_types = [
            'StrSchema', 'BoolSchema', 'IntSchema', 'FloatSchema', 'NoneSchema',
            'BytesSchema', 'NoneSchema', 'DateTimeSchema',
            'NumericSchema', 'UUIDStrSchema', 'UUID4Schema'
        ]
        return schema_.class_name in scalar_types

    def generate_pyi(self) -> Tuple[list[ast.AnnAssign], list[Import]]:
        annotation = annotated_assign(self.name, type(self.value).__name__)
        imports = [Import(get_module_to_import_from(self.value), self.class_name)]
        return [annotation], imports
