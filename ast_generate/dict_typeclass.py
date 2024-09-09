import ast
from typing import Any

from ast_generate.dict_value_type import AnyDictValueType


def generate_key_typing_assign(name: str, type_: Any) -> ast.AnnAssign:
    return ast.AnnAssign(
        target=ast.Name(id=name),
        annotation=type_.get_type_for_typeclass(),
        value=None,
        simple=1
    )


def dict_typeclass(name: str, meta_name: str, typing_map: dict[str, AnyDictValueType]):
    return ast.ClassDef(
        name=f"{name}",
        bases=[],
        body=[
            ast.ClassDef(
                name="type",
                bases=[ast.Name(id="TypedDict", ctx=ast.Load())],
                keywords=[ast.keyword(arg='total', value=ast.NameConstant(value=False))],
                body=[
                    generate_key_typing_assign(name, type_)
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
