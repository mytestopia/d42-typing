import typing


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
