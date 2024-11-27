import ast
from keyword import iskeyword
from typing import Dict, Tuple

from niltype import Nil

import ast_generate
from app.helpers import (
    get_module_to_import_from,
    get_types_from_any,
    is_builtin_class_instance,
    is_dict_typed_as_empty,
)
from app.modules.module import Import
from app.types._type import OverloadedFake, Typing, UnknownTypeSchema
from ast_generate import annotated_assign
from ast_generate.dict_value_type import (
    DictValueSubDictSimpleType,
    DictValueSubDictType,
    DictValueUnionType,
    ScalarDictValueType,
)


class DictTyping(Typing):

    @classmethod
    def is_valid_type_for_schema(cls, schema_: UnknownTypeSchema) -> bool:
        return schema_.class_name == 'DictSchema'

    def update_name(self, name: str):
        self.name = name

    def generate_pyi_empty_dict(self) -> Tuple[list[ast.AnnAssign], list[Import]]:
        annotation = annotated_assign(self.name, type(self.value).__name__)
        import_ = Import(get_module_to_import_from(self.value), self.value.__class__.__name__)
        return [annotation], [import_]

    def generate_pyi(self) -> Tuple[list[ast.expr | ast.AnnAssign], list[Import]]:
        imports = []
        annotations = []

        # todo для nested dict типизация присутствует дважды

        if is_dict_typed_as_empty(self.value):
            return self.generate_pyi_empty_dict()

        typing_map = {}

        for item in ['overload', 'Literal', 'TypedDict']:
            imports.append(Import('typing', item))

        for key, item_value in self.value.props.keys.items():
            value_, _ = item_value
            value_as_class = UnknownTypeSchema(key, value_)

            # если значение словаря само является словарем
            if DictTyping.is_valid_type_for_schema(value_as_class):
                sub_dict_schema = DictTyping(key, value_)

                if is_dict_typed_as_empty(sub_dict_schema.value):
                    imports.append(Import('typing', 'Dict'))
                    typing_map[key] = DictValueSubDictSimpleType(Dict)

                else:
                    sub_dict_schema.update_name(f'{self.name}_{key.capitalize()}Schema')

                    nested_annotations, nested_imports = sub_dict_schema.generate_pyi()
                    annotations.extend(nested_annotations)
                    imports.extend(nested_imports)

                    typing_map[key] = DictValueSubDictType(sub_dict_schema.name)

            elif (
                    value_.type is not None
                    and not is_builtin_class_instance(value_.type)
            ):
                value_type = value_.type

                if hasattr(value_type, 'type') and is_builtin_class_instance(value_type.type):
                    imports.append(
                        Import(get_module_to_import_from(value_.type), value_.type.__name__))
                    typing_map[key] = ScalarDictValueType(value_.type)

                # когда value = schema.any(...)
                elif value_.__class__.__name__ == 'AnySchema':

                    if value_.props.types is not Nil:
                        types_in_any = get_types_from_any(value_.props)

                        if len(types_in_any) == 1:
                            type_ = types_in_any.pop()
                            imports.append(Import(get_module_to_import_from(type_), type_.__name__))
                            typing_map[key] = ScalarDictValueType(type_)

                        else:
                            imports.append(Import('typing', 'Union'))
                            for type_ in types_in_any:
                                imports.append(
                                    Import(get_module_to_import_from(type_), type_.__name__))
                            typing_map[key] = DictValueUnionType(types_in_any)

                    else:
                        # когда value = schema.any
                        imports.append(Import(get_module_to_import_from(value_), value_.__class__.__name__))
                        typing_map[key] = ScalarDictValueType(value_.__class__)

                else:
                    # когда value = typing.Any
                    imports.append(
                        Import(get_module_to_import_from(value_.type), value_type.__name__))
                    typing_map[key] = DictValueSubDictSimpleType(value_type)

            else:
                imports.append(
                    Import(get_module_to_import_from(value_), value_.__class__.__name__))
                typing_map[key] = ScalarDictValueType(value_.__class__)

        meta_class_name = f'_D42Meta{self.name}'
        annotations.append(ast_generate.dict_metaclass(meta_class_name, typing_map))

        dict_typeclass_generator = ast_generate.dict_typeclass_v2 if any(
            iskeyword(key) for key in typing_map.keys()) else ast_generate.dict_typeclass

        annotations.append(dict_typeclass_generator(self.name, meta_class_name, typing_map))

        return annotations, imports

    def generate_fake_overload(self, path_to_schema: str) -> Tuple[OverloadedFake, list[Import]]:

        if is_dict_typed_as_empty(self.value):
            imports = [
                Import('typing', 'Dict'),
                Import(get_module_to_import_from(self.value), self.class_name)
            ]
            overload = OverloadedFake(
                self.class_name,
                ast_generate.fake_scalar_overload(self.class_name, self.class_type)
            )
            return overload, imports

        module_name = path_to_schema.replace('/', '.').replace('.py', '')
        imports = [
            Import('typing', 'Type'),
            Import(module_name, self.name),
        ]
        overload = OverloadedFake(
            self.name,
            ast_generate.fake_dict_overload(self.name)
        )
        return overload, imports
