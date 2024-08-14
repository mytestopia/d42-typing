import ast
from typing import Any

from ast_generate.dict_value_type import AnyDictValueType


def get_getitem_method_return_ast(type_schema: Any) -> Any:
    """
    Возвращает ast-тип возвращаемого значения метода __getitem__.
    """
    return type_schema.get_type_for_metaclass()


def getitem_method(key_name: str, type_schema: Any, keys_count: int):
    """
    Возвращает ast-метод, используемый в мета-классе для типизации словаря:
    @overload
    def __getitem__(cls, arg: Literal["id"]) -> IntSchema:
        pass
    """
    decorators_list = [ast.Name(id='overload')] if keys_count > 1 else []
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
        decorator_list=decorators_list,
        returns=get_getitem_method_return_ast(type_schema)
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


def dict_metaclass(name: str, typing_map: dict[str, AnyDictValueType]):
    """
    Возвращает ast-класс, используемый в мета-классе для типизации словаря.
    Пример:
    class _D42MetaObjectSchema(type):

        @overload
        def __getitem__(cls, arg: Literal['id']) -> int:
            pass

        @overload
        def __getitem__(cls, arg: Literal['name']) -> str:
            pass

        def __mod__(self, other):
            pass

        def __add__(self, other):
            pass
    """
    return ast.ClassDef(
        name=f"{name}",  # gen_unique_name
        bases=[ast.Name(id="type")],
        body=[
                 getitem_method(key, value, len(typing_map.keys()))
                 for key, value in typing_map.items()
             ] + schema_substitution_methods(),
        keywords=[],
        decorator_list=[]
    )
