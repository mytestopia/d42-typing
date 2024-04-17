import ast


def getitem_method(key_name: str, type_schema: str):
    """
    Возвращает ast-метод, используемый в мета-классе для типизации словаря:
    @overload
    def __getitem__(cls, arg: Literal["id"]) -> IntSchema:
        pass
    """
    return ast.FunctionDef(
        name='__getitem__',
        args=[
            ast.arguments(
                posonlyargs=[],
                args=[
                    ast.arg(arg='cls'),
                    ast.arg(
                        arg='arg',
                        annotation=ast.Subscript(
                            value=ast.Name(id='Literal'),
                            slice=ast.Constant(value=key_name, kind=None),
                        ),
                        type_comment=None,
                    ),
                ],
                defaults=[],
                kwonlyargs=[]
            )
        ],
        body=[ast.Pass()],
        decorator_list=[ast.Name(id='overload')],
        returns=ast.Name(id=str(type_schema)),
    )


def dict_metaclass(name: str, typing_map: dict[str, str]):
    """Возвращает ast-класс, используемый в мета-классе для типизации словаря"""
    return ast.ClassDef(
        name=f"_{name}",  # gen_unique_name
        bases=[ast.Name(id="type")],
        body=[getitem_method(key, value) for key, value in typing_map.items()],
        keywords=[],
        decorator_list=[]
    )
