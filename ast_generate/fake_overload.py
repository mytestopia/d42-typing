import ast


def _fake_overload(annotation, returns):
    return ast.FunctionDef(
        name='fake',
        args=ast.arguments(
            posonlyargs=[],
            args=[ast.arg(
                arg='schema',
                annotation=annotation,
                type_comment=None,
            )],
            vararg=None,
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=None,
            defaults=[]
        ),
        body=[ast.Pass()],
        decorator_list=[ast.Name(id='overload')],
        returns=returns
    )


def fake_none_overload(type_schema: str):
    """
    Возвращает метод перегрузки для скалярных типов:
    @overload
    def fake(schema: NoneSchema) -> None: pass
    """
    return _fake_overload(
        annotation=ast.Name(id=type_schema),
        returns=ast.Name(id='None')
    )


def fake_scalar_overload(type_schema: str, type_: str):
    """
    Возвращает метод перегрузки для скалярных типов:
    @overload
    def fake(schema: IntSchema) -> int: pass
    """
    return _fake_overload(
        annotation=ast.Name(id=type_schema),
        returns=ast.Name(id=type_.__name__),
    )


def fake_dict_overload(schema_name: str):
    """
    Возвращает метод перегрузки для сложных типов:
    @overload
    def fake(schema: Type[NameSchema]) -> NameSchema.type: pass
    """
    return _fake_overload(
        annotation=ast.Subscript(
            value=ast.Name(id='Type'),
            slice=ast.Name(id=schema_name),
        ),
        returns=ast.Attribute(value=ast.Name(id=schema_name), attr='type')
    )


def fake_list_overload(schema_name: str, item_type: str):
    """
    Возвращает метод перегрузки для сложных типов:
    @overload
    def fake(schema: Type[NameSchema]) -> list[str]
    """
    return _fake_overload(
        annotation=ast.Subscript(
            value=ast.Name(id='Type'),
            slice=ast.Name(id=schema_name),
        ),
        returns=ast.Subscript(
            value=ast.Name(id='list'),
            slice=ast.Name(id=item_type)
        )
    )
