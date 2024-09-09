import ast
from typing import Tuple

from niltype import Nil

import ast_generate
from app.helpers import get_module_to_import_from, get_types_from_any
from app.modules.module import Import
from app.types._type import OverloadedFake, Typing, UnknownTypeSchema


class AnyTyping(Typing):

    @classmethod
    def is_valid_type_for_schema(cls, schema_: UnknownTypeSchema) -> bool:
        return schema_.class_name == 'AnySchema'

    def generate_pyi(self) -> Tuple[list[ast.AnnAssign], list[Import]]:
        imports = []
        annotations = []

        if hasattr(self.value.props, 'types') and self.value.props.types is not Nil:
            types_in_any = get_types_from_any(self.value.props)

            if len(types_in_any) == 1:
                type_ = types_in_any.pop()

                if type_.__name__ == 'DictSchema':
                    ...
                    # todo union для словарей
                imports.append(Import(get_module_to_import_from(type_), type_.__name__))
                annotations.append(ast_generate.annotated_assign(self.name, type_.__name__))
                return annotations, imports

            else:
                imports.append(Import('typing', 'Union'))
                for type_ in types_in_any:
                    imports.append(Import(get_module_to_import_from(type_), type_.__name__))
                annotations.append(ast_generate.annotated_assign_union(self.name, types_in_any))
                return annotations, imports

        imports.append(Import('district42.types', 'AnySchema'))
        annotations.append(ast_generate.annotated_assign(self.name, 'AnySchema'))
        return annotations, imports

    def generate_fake_overload(self,  path_to_schema: str) -> Tuple[OverloadedFake, list[Import]]:
        imports = []
        if self.value.props.types is not Nil:
            types_in_any = get_types_from_any(self.value.props)

            if len(types_in_any) == 1:
                type_ = types_in_any[0]
                class_name = type_.__name__
                imports.append(Import(get_module_to_import_from(type_), class_name))
                overload = OverloadedFake(
                    class_name,
                    ast_generate.fake_scalar_overload(class_name, type_.type)
                )
                return overload, imports

            else:
                module_name = path_to_schema.replace('/', '.').replace('.py', '')
                imports.extend([
                    Import('typing', 'Union'),
                    Import(module_name, self.name),
                ])
                overload = OverloadedFake(
                    self.name,
                    ast_generate.fake_union_overload(self.name, types_in_any)
                )
                return overload, imports

        imports.append(Import('typing', 'Any'))
        imports.append(Import(get_module_to_import_from(self.value), 'AnySchema'))
        overload = OverloadedFake(
            'AnySchema',
            ast_generate.fake_scalar_overload('AnySchema', self.value.__class__.type)
        )
        return overload, imports
