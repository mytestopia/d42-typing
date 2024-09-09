import typing

from d42.custom_type import CustomSchema
from district42.types import AnyProps


def is_builtin_class_instance(obj):
    return obj.__module__ == 'builtins'


def is_schema_type_simple(schema_value: typing.Any) -> bool:
    """Т.е. тип схемы не является пользовательским классом."""
    # для NoneSchema нельзя метод is_builtin_class_instance падает с исключением
    return (
            schema_value.type is None
            or schema_value.type is typing.Any
            or schema_value.type is typing.Dict
            or schema_value.type is typing.List
            or is_builtin_class_instance(schema_value.type)
    )


def get_module_to_import_from(schema_value: typing.Any) -> str:

    def remove_protected_prefix(module_name: str) -> str:
        """district42.types._any_schema -> district42.types"""
        parts = module_name.split('.')
        filtered_parts = [part for part in parts if not part.startswith('_')]
        return '.'.join(filtered_parts)

    import_from = schema_value.__module__
    return remove_protected_prefix(import_from)


def get_types_from_any(any_value_props) -> list[typing.Any]:
    types_list = list()
    for type_ in any_value_props.types:
        if issubclass(type_.__class__, CustomSchema):
            if (
                hasattr(type_, 'type') is False
                or type_.type is typing.Any
            ):
                types_list.append(typing.Any)
            else:
                types_list.append(type_.type)

        elif isinstance(type_.props, AnyProps):
            types_list.extend(get_types_from_any(type_.props))

        else:
            types_list.append(type_.__class__)

    unique_types = []
    [unique_types.append(x) for x in types_list if x not in unique_types]
    return unique_types
