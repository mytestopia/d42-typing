import ast
import typing
from typing import Tuple

import ast_generate
from app.helpers import get_module_to_import_from
from app.modules.module import Import
from app.types._type import OverloadedFake, Typing, UnknownTypeSchema
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

    def generate_fake_overload(self,  path_to_schema: str) -> Tuple[OverloadedFake, list[Import]]:
        imports = []

        imports.append(Import(get_module_to_import_from(self.value), self.class_name))
        if self.class_name == 'NoneSchema':
            overload = OverloadedFake(
                self.class_name,
                ast_generate.fake_none_overload(self.class_name)
            )
            return overload, imports

        elif self.value.type is typing.Any:
            imports.append(Import('typing', 'Any'))
            overload = OverloadedFake(
                typing.Any,
                ast_generate.fake_scalar_overload(self.class_name, typing.Any)
            )
            return overload, imports

        overload = OverloadedFake(
            self.class_name,
            ast_generate.fake_scalar_overload(self.class_name, self.value.__class__.type)
        )

        return overload, imports
