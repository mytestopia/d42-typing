import ast
from typing import Tuple

from niltype import Nil

import ast_generate
from app.helpers import get_module_to_import_from
from app.modules.module import Import
from app.types._type import OverloadedFake, Typing, UnknownTypeSchema


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

    def generate_fake_overload(self,  path_to_schema: str) -> Tuple[OverloadedFake, list[Import]]:
        imports = [Import('typing', 'List')]

        if self.value.props.type is not Nil:
            list_item_type = self.value.props.type.type
            list_item_type_name = list_item_type.__name__

            module_name = path_to_schema.replace('/', '.').replace('.py', '')
            imports.extend([
                Import(module_name, self.name),
                Import('typing', 'Type')
            ])
            overload = OverloadedFake(
                self.class_name,
                ast_generate.fake_list_overload(self.name, list_item_type_name)
            )
            return overload, imports

        imports.append(Import(get_module_to_import_from(self.value), 'ListSchema'))
        overload = OverloadedFake(
            'ListSchema',
            ast_generate.fake_scalar_overload('ListSchema', self.value.__class__.type)
        )
        return overload, imports
