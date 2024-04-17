import typing

from niltype import Nil

import ast_generate
from app.helpers import get_module_to_import_from, is_builtin_class_instance
from app.modules.module import Module


class OverloadedFake:
    def __init__(self, schema_type, ast_method):
        self.schema_type = schema_type
        self.ast_method = ast_method

    def __eq__(self, other):
        return self.schema_type == other.schema_type


class BlahBlahModule(Module):
    def __init__(self):
        super().__init__('blahblah.py')
        self.add_import('typing', 'overload')
        self.overloaded_fakes = []

    def _add_overload(self, schema_type, overloaded_fake):
        method = OverloadedFake(schema_type, overloaded_fake)
        if method not in self.overloaded_fakes:
            self.overloaded_fakes.append(method)

    def get_ast_content(self) -> list:
        return [
            import_.to_ast() for import_ in self.imports
        ] + [
            fake.ast_method for fake in self.overloaded_fakes
        ]

    def _generate_scalar_overload(self, input_type, output_type, schema_value):
        """Добавляет fake(schema: <input_type>) -> <output_type>"""
        self.add_import(get_module_to_import_from(schema_value), input_type)
        self._add_overload(
            input_type,
            ast_generate.fake_scalar_overload(input_type, output_type)
        )

    def _generate_overload_NoneSchema(self, schema_value):
        """Добавляет fake(schema: NoneSchema) -> None"""
        schema_name = schema_value.__class__.__name__  # NoneSchema
        self.add_import(get_module_to_import_from(schema_value), schema_name)
        self._add_overload(
            schema_name,
            ast_generate.fake_none_overload(schema_name)
        )

    def _generate_overload_DictSchema(self, path_to_schema, schema_name, schema_value):
        if schema_value.props.keys is Nil:
            self._generate_scalar_overload(schema_value.__class__.__name__, schema_value.__class__.type, schema_value)
            return

        self.add_import('typing', 'Type')
        module_name = path_to_schema.replace('/', '.').replace('.py', '')
        self.add_import(module_name, schema_name)
        self._add_overload(
            schema_name,
            ast_generate.fake_dict_overload(schema_name)
        )

    def _generate_overload_ListSchema(self, path_to_schema, schema_name, schema_value):
        if schema_value.props.type is not Nil:
            list_item_type = schema_value.props.type.type
            list_item_type_name = list_item_type.__name__

            module_name = path_to_schema.replace('/', '.').replace('.py', '')
            self.add_import(module_name, schema_name)

            self.add_import('typing', 'Type')
            self._add_overload(
                schema_name,
                ast_generate.fake_list_overload(schema_name, list_item_type_name)
            )
        else:
            self._generate_scalar_overload('ListSchema', schema_value.__class__.type, schema_value)

    def _generate_overload_AnySchema(self, any_value):
        if any_value.props.types is not Nil:
            types_set = set(type.type for type in any_value.props.types)

            if len(types_set) == 1:
                type_ = any_value.props.types[0]
                class_name = type_.__class__.__name__
                self._generate_scalar_overload(class_name, type_.type, type_)
                return

        self.add_import('typing', 'Any')
        self._generate_scalar_overload('AnySchema', any_value.__class__.type, any_value)

    def _generate_builtin_type(self, schema_name, schema_type_name, file_name, schema_value):

        if schema_type_name == 'DictSchema':
            self._generate_overload_DictSchema(file_name, schema_name, schema_value)

        elif schema_type_name == 'NoneSchema':
            self._generate_overload_NoneSchema(schema_value)

        elif schema_type_name == 'NumericSchema':
            self._generate_scalar_overload(schema_type_name, str, schema_value)

        elif schema_type_name == 'AnySchema':
            self._generate_overload_AnySchema(schema_value)

        elif schema_type_name == 'ListSchema':
            self._generate_overload_ListSchema(file_name, schema_name, schema_value)

        else:
            self._generate_scalar_overload(schema_type_name, schema_value.__class__.type, schema_value)

    def generate(self, file_name, schema_name, schema_value):
        # для NoneSchema нельзя метод is_builtin_class_instance падает с исключением
        if (schema_value.type is None or schema_value.type is typing.Any or
                is_builtin_class_instance(schema_value.type)):

            schema_type_name = schema_value.__class__.__name__
            self._generate_builtin_type(schema_name, schema_type_name, file_name, schema_value)
            return

        schema_type_name = schema_value.type.__name__
        self._generate_scalar_overload(
            input_type=schema_type_name,
            output_type=schema_value.type.type,
            schema_value=schema_value)
