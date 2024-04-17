import ast


def dict_typeclass(name: str, typing_map: dict[str, str]):
    return ast.ClassDef(
        name=f"{name}",
        bases=[],
        body=[
            ast.ClassDef(
                name="type",
                bases=[ast.Name(id="TypedDict", ctx=ast.Load())],
                keywords=[ast.keyword(arg='total', value=ast.NameConstant(value=False))],
                body=[
                    ast.AnnAssign(
                        target=ast.Name(id=name),
                        annotation=ast.Attribute(
                            value=ast.Name(id=type_),
                            attr='type',
                        ),
                        simple=1,
                    )
                    for name, type_ in typing_map.items()
                ],
                decorator_list=[],
            )
        ],
        keywords=[ast.keyword(arg="metaclass", value=ast.Name(id=f"_{name}"))],
        decorator_list=[],
        starargs=None,
        kwargs=None,
    )
