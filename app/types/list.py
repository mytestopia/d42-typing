import ast
from typing import Any, Tuple

from niltype import Nil

import ast_generate
from app.helpers import get_module_to_import_from, get_types_from_any
from app.modules.module import Import
from app.types._type import Typing, UnknownTypeSchema


class ListTyping(Typing):

    @classmethod
    def is_valid_type_for_schema(cls, schema_: UnknownTypeSchema) -> bool:
        return schema_.class_name == 'ListSchema'

    def generate_pyi(self) -> Tuple[list[ast.AnnAssign], list[Import]]:

        if self.value.props.type is not Nil:
            item_type = self.value.props.type
            item_type_class_name = self.value.props.type.__class__.__name__

            imports = [
                Import('typing', 'List'),
                Import(get_module_to_import_from(item_type), item_type_class_name)
            ]
            annotation = ast_generate.list_typeclass(self.name, item_type_class_name)
            return [annotation], imports

        annotation = ast_generate.annotated_assign(self.name, type(self.value).__name__)
        import_ = Import(get_module_to_import_from(self.value), self.value.__class__.__name__)
        
        return [annotation], [import_]

