import typing
from d42.custom_type import Schema
from niltype import Nil

import ast_generate
from app.helpers import get_module_to_import_from, is_builtin_class_instance, is_schema_type_simple

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

    def _generate_typing_DictSchema(self, dict_name: str, dict_value):
        typing_map = {}
        # todo для nested dict типизация присутствует дважды

        def has_invalid_key(dictionary: dict) -> bool:
            # TODO очень костыльная проверка, нужен метод в общем виде
            for key in dictionary.keys():
                if '[' in key:
                    return True
            return False

        # схема словаря без ключей (schema.dict)
        if (
                dict_value.props.keys is Nil
                or has_invalid_key(dict_value.props.keys)
        ):
            self._generate_scalar_typing(dict_name, dict_value.__class__.__name__, dict_value)
            return

        self.add_import('typing', 'overload', 'Literal', 'TypedDict')
        for key, item_value in dict_value.props.keys.items():
            value_schema, _ = item_value
            value_type = value_schema.__class__

            if value_type.__name__ == 'DictSchema':
                nested_dict_schema_name = f'{dict_name}_{key.capitalize()}Schema'
                self._generate_typing_DictSchema(nested_dict_schema_name, value_schema)
                typing_map[key] = nested_dict_schema_name

            elif value_schema.type is not None and not is_builtin_class_instance(value_schema.type):
                value_type = value_schema.type
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
            types_set = set(type.type for type in any_value.props.types)

            if len(types_set) == 1:
                type_ = any_value.props.types[0]
                class_name = type_.__class__.__name__
                self._generate_scalar_typing(any_name, class_name, type_)
                return

        self.add_import('district42.types', 'AnySchema')
        self._generate_scalar_typing(any_name, 'AnySchema', any_value)

    def _generate_scalar_typing(self, schema_name: str, schema_type: str, schema_value: typing.Any):
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
            return

        # для кастомных схем, у которых не прописан тип:
        if schema_value.type is typing.Any and schema_value.__class__.__name__.startswith('_'):
            self.add_import('district42.types', 'AnySchema')
            self._add_typing(ast_generate.annotated_assign(schema_name, 'AnySchema'))
            return

        if is_schema_type_simple(schema_value):
            schema_type_name = schema_value.__class__.__name__
            self._generate_builtin_type(schema_name, schema_type_name, schema_value)
            return

        schema_type_name = schema_value.type.__name__
        self._generate_builtin_type(schema_name, schema_type_name, schema_value.type)
