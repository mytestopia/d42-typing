import typing

from d42.custom_type import CustomSchema, Schema
from niltype import Nil

import ast_generate
from app.helpers import (
    get_module_to_import_from,
    get_types_from_any,
    has_invalid_key,
    is_builtin_class_instance,
    is_dict_empty,
    is_dict_without_keys,
    is_schema_type_simple,
)
from ast_generate import annotated_assign

from .module import Module


class TypedModule(Module):

    def _add_typing(self, item):
        self.typed_items.append(item)

    def get_ast_content(self) -> list[str] | None:
        imports = [import_.to_ast() for import_ in self.imports]
        items = self.typed_items
        if items:
            return imports + items
        return None

    def _generate_typing_empty_dict(self, dict_name, dict_value):
        return self._generate_scalar_typing(dict_name, dict_value.__class__.__name__, dict_value)

    def _generate_typing_DictSchema(self, dict_name: str, dict_value):
        typing_map = {}
        # todo для nested dict типизация присутствует дважды

        if (
                is_dict_without_keys(dict_value)
                or is_dict_empty(dict_value)
                or has_invalid_key(dict_value.props.keys)
        ):
            self._generate_typing_empty_dict(dict_name, dict_value)
            return

        self.add_import('typing', 'overload', 'Literal', 'TypedDict')
        for key, item_value in dict_value.props.keys.items():
            value_schema, _ = item_value
            value_type = value_schema.__class__

            if value_type.__name__ == 'DictSchema':
                if (
                        is_dict_without_keys(value_schema)
                        or is_dict_empty(value_schema)
                        or has_invalid_key(value_schema.props.keys)
                ):
                    self.add_import('typing', 'Dict')
                    typing_map[key] = value_schema.type
                else:
                    nested_dict_schema_name = f'{dict_name}_{key.capitalize()}Schema'
                    self._generate_typing_DictSchema(nested_dict_schema_name, value_schema)
                    typing_map[key] = nested_dict_schema_name

            elif (
                    value_schema.type is not None
                    and not is_builtin_class_instance(value_schema.type)
            ):
                value_type = value_schema.type

                if value_schema.__class__.__name__ == 'AnySchema':
                    types_in_any = get_types_from_any(value_schema.props)

                    if len(types_in_any) == 1:
                        type_ = types_in_any.pop()
                        self.add_import(get_module_to_import_from(type_), type_.__name__)
                        typing_map[key] = type_

                    else:
                        # todo
                        self.add_import('typing', 'Union')
                        for type_ in types_in_any:
                            self.add_import(get_module_to_import_from(type_), type_.__name__)
                        self.add_import(get_module_to_import_from(value_schema.type),
                                        value_type.__name__)
                        typing_map[key] = value_type
                        # self._add_typing(
                        #     ast_generate.annotated_assign_union(any_name, types_in_any))

                else:
                    self.add_import(get_module_to_import_from(value_schema.type), value_type.__name__)
                    typing_map[key] = value_type

            else:
                self.add_import(get_module_to_import_from(value_schema), value_type.__name__)
                typing_map[key] = value_type

        meta_class_name = f'_D42Meta{dict_name}'
        self._add_typing(ast_generate.dict_metaclass(meta_class_name, typing_map))
        self._add_typing(ast_generate.dict_typeclass(dict_name, meta_class_name, typing_map))

    def _generate_typing_ListSchema(self, list_name: str, list_value):
        if list_value.props.type is not Nil:
            item_type = list_value.props.type
            item_type_class_name = list_value.props.type.__class__.__name__

            self.add_import('typing', 'List')
            self.add_import(get_module_to_import_from(item_type), item_type_class_name)

            self._add_typing(ast_generate.list_typeclass(list_name, item_type_class_name))
            return

        self._generate_scalar_typing(list_name, 'ListSchema', list_value)

    def _generate_typing_AnySchema(self, any_name: str, any_value):

        if hasattr(any_value.props, 'types') and any_value.props.types is not Nil:
            types_in_any = get_types_from_any(any_value.props)

            if len(types_in_any) == 1:
                type_ = types_in_any.pop()

                if type_.__name__ == 'DictSchema':
                    ...
                    # todo union для словарей
                self._generate_scalar_typing(any_name, type_.__name__, type_)
                return

            else:
                self.add_import('typing', 'Union')
                for type_ in types_in_any:
                    self.add_import(get_module_to_import_from(type_), type_.__name__)
                self._add_typing(ast_generate.annotated_assign_union(any_name, types_in_any))
                return

        self.add_import('district42.types', 'AnySchema')
        self._generate_scalar_typing(any_name, 'AnySchema', any_value)

    def _generate_scalar_typing(self, schema_name: str, schema_type: str,
                                schema_value: typing.Any):
        self.add_import(get_module_to_import_from(schema_value), schema_type)
        self._add_typing(ast_generate.annotated_assign(schema_name, schema_type))

    def _generate_builtin_type(self, schema_name, schema_type_name, schema_value):
        """Для стандартных схем"""
        if schema_type_name == 'DictSchema':
            self._generate_typing_DictSchema(schema_name, schema_value)

        elif schema_type_name == 'AnySchema':
            self._generate_typing_AnySchema(schema_name, schema_value)

        elif schema_type_name == 'ListSchema':
            self._generate_typing_ListSchema(schema_name, schema_value)

        else:
            self._generate_scalar_typing(schema_name, schema_type_name, schema_value)

    def generate(self, schema_name: str, schema_value: typing.Any):
        if not isinstance(schema_value, Schema):
            if is_builtin_class_instance(type(schema_value)):
                self._add_typing(annotated_assign(schema_name, type(schema_value).__name__))
            return
        # для кастомных схем, у которых не прописан тип:
        if (
                issubclass(schema_value.__class__, CustomSchema)
                and (hasattr(schema_value, 'type') is False
                     or schema_value.type is typing.Any)
        ):
            return

        if is_schema_type_simple(schema_value):
            schema_type_name = schema_value.__class__.__name__
            self._generate_builtin_type(schema_name, schema_type_name, schema_value)
            return

        schema_type_name = schema_value.type.__name__
        self._generate_builtin_type(schema_name, schema_type_name, schema_value.type)
