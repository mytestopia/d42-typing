import ast


def annotated_assign(name: str, type_: str):
    """return annotation assign like: name: type"""
    return ast.AnnAssign(
        target=ast.Name(id=name),
        annotation=ast.Name(id=type_),
        simple=1,
    )
