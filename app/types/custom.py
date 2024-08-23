import ast
import typing
from typing import Tuple

from d42.custom_type import CustomSchema
from district42 import Schema

import ast_generate
from app.helpers import get_module_to_import_from
from app.modules.module import Import
from app.types._type import OverloadedFake, Typing, UnknownTypeSchema
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

    def generate_fake_overload(self,  path_to_schema: str) -> Tuple[OverloadedFake, list[Import]]:
        # для кастомных схем, у которых не прописан тип:
        if (
            hasattr(self.value, 'type') is False
            or self.value.type is typing.Any
        ):
            registered_type_name = self.value.__class__.__name__
            imports = [
                Import('typing', 'Any'),
                Import(get_module_to_import_from(self.value), registered_type_name)
            ]
            overload = OverloadedFake(typing.Any,
                                      ast_generate.fake_scalar_overload(
                                          registered_type_name, typing.Any))
            return overload, imports

        else:
            if issubclass(self.class_type, Schema):
                imports = [
                    Import(get_module_to_import_from(self.class_type), self.class_name)
                ]
                overload = OverloadedFake(self.class_name,
                                          ast_generate.fake_scalar_overload(self.class_name,
                                                                            self.class_type.type))
                return overload, imports
            else:
                # todo
                pass
            pass
        return None, []
