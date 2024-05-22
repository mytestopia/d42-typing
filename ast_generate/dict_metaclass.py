import ast
from typing import Any


def getitem_method(key_name: str, type_schema: Any):
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
        # FIXME для вложенных словорей type_schema строка, для остальных - объект
        returns=ast.Name(id=str(type_schema.__name__) if hasattr(type_schema, '__name__') else type_schema),
    )


def schema_substitution_methods() -> list[ast.FunctionDef]:
    """
    Возвращает список ast-методов, используемый в мета-классе для типизации словаря:
    def __mod__(self, other): pass
    def __add__(self, other): pass
    """
    def ast_method(name: str) -> ast.FunctionDef:
        return ast.FunctionDef(
            name=name,
            args=[
                ast.arguments(
                    posonlyargs=[],
                    args=[ast.arg(arg='self'), ast.arg(arg='other')],
                    defaults=[],
                    kwonlyargs=[]
                )
            ],
            body=[ast.Pass()],
            decorator_list=[],
        )
    return [ast_method(name) for name in ['__mod__', '__add__']]


def dict_metaclass(name: str, typing_map: dict[str, Any]):
    """Возвращает ast-класс, используемый в мета-классе для типизации словаря"""
    return ast.ClassDef(
        name=f"{name}",  # gen_unique_name
        bases=[ast.Name(id="type")],
        body=[getitem_method(key, value) for key, value in typing_map.items()] +
             schema_substitution_methods(),
        keywords=[],
        decorator_list=[]
    )
