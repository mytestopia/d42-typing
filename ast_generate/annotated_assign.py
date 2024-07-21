import ast


def annotated_assign(name: str, type_: str) -> ast.AnnAssign:
    """return annotation assign like: name: type"""
    return ast.AnnAssign(
        target=ast.Name(id=name),
        annotation=ast.Name(id=type_),
        simple=1,
    )


def annotated_assign_union(schema_name: str, types_in_union: list[str | None]) -> ast.AnnAssign:
    return ast.AnnAssign(
        target=ast.Name(id=schema_name),
        annotation=ast.Subscript(
            value=ast.Name(id='Union'),
            slice=ast.Tuple(
                elts=[
                    ast.Name(id=type_.__name__) for type_ in types_in_union
                ],
            ),
        ),
        simple=1,
    )
