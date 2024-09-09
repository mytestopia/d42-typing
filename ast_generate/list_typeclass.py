import ast


def list_typeclass(name: str, item_type: str):
    """
    class NameSchema: type = List[item_type.type]
    """
    return ast.ClassDef(
        name=f"{name}",
        bases=[],
        body=[
            ast.Assign(
                targets=[ast.Name(id='type')],
                value=ast.Subscript(
                    value=ast.Name(id='List'),
                    slice=ast.Attribute(
                        value=ast.Name(id=item_type),
                        attr='type',
                    )
                ),
            )
        ],
        keywords=[],
        decorator_list=[],
        starargs=None,
        kwargs=None,
    )
