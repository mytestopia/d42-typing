import ast
from typing import Any


def generate_ann_assign(name: str, type_: Any) -> ast.AnnAssign:
    if type(type_).__module__ == 'typing':
        return ast.AnnAssign(
            target=ast.Name(id=name),
            annotation=ast.Name(id=type_.__name__),
            value=None,
            simple=1,
        )

    return ast.AnnAssign(
        target=ast.Name(id=name),
        annotation=ast.Attribute(
            # FIXME для вложенных словарей type_ строка, для остальных - объект
            value=ast.Name(id=type_.__name__ if hasattr(type_, '__name__') else type_),
            attr='type',
        ),
        simple=1,
    )


def dict_typeclass(name: str, meta_name: str, typing_map: dict[str, str]):
    return ast.ClassDef(
        name=f"{name}",
        bases=[],
        body=[
            ast.ClassDef(
                name="type",
                bases=[ast.Name(id="TypedDict", ctx=ast.Load())],
                keywords=[ast.keyword(arg='total', value=ast.NameConstant(value=False))],
                body=[
                    generate_ann_assign(name, type_)
                    for name, type_ in typing_map.items()
                ],
                decorator_list=[],
            )
        ],
        keywords=[ast.keyword(arg="metaclass", value=ast.Name(id=meta_name))],
        decorator_list=[],
        starargs=None,
        kwargs=None,
    )

