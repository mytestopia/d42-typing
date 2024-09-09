import ast


class AnyDictValueType:

    def get_type_for_typeclass(self):
        pass

    def get_type_for_metaclass(self):
        pass


class ScalarDictValueType(AnyDictValueType):
    def __init__(self, type_):
        self.type_ = type_

    def get_type_for_typeclass(self) -> ast.Attribute:
        """ : IntSchema.type"""
        return ast.Attribute(
            value=ast.Name(id=self.type_.__name__),
            attr='type',
        )

    def get_type_for_metaclass(self) -> ast.Name:
        """ -> IntSchema"""
        return ast.Name(id=self.type_.__name__)


class DictValueUnionType(AnyDictValueType):
    def __init__(self, types_in_union):
        self.types_in_union = types_in_union

    def get_type_for_typeclass(self) -> ast.Subscript:
        """: Union[IntSchema.type, NoneSchema.type] """
        return ast.Subscript(
            value=ast.Name(id='Union'),
            slice=ast.Tuple(
                elts=[
                    ast.Attribute(
                        value=ast.Name(id=schema_in_union.__name__),
                        attr='type'
                    )
                    for schema_in_union in self.types_in_union
                ]
            )
        )

    def get_type_for_metaclass(self) -> ast.Subscript:
        """-> Union[IntSchema, NoneSchema]"""
        return ast.Subscript(
            value=ast.Name(id='Union'),
            slice=ast.Tuple(
                elts=[
                    ast.Name(id=schema_in_union.__name__)
                    for schema_in_union in self.types_in_union
                ]
            )
        )


class DictValueSubDictType(AnyDictValueType):

    def __init__(self, name):
        self.name = name

    def get_type_for_metaclass(self) -> ast.Name:
        """-> NestedTestSchema_EntitySchema"""
        return ast.Name(id=self.name)

    def get_type_for_typeclass(self) -> ast.Attribute:
        """-> NestedTestSchema_EntitySchema.type"""
        return ast.Attribute(
            value=ast.Name(id=self.name),
            attr='type',
        )


class DictValueSubDictSimpleType(AnyDictValueType):

    def __init__(self, type_):
        self.type_ = type_

    def get_type_for_metaclass(self) -> ast.Name:
        """ -> Dict"""
        return ast.Name(id=self.type_.__name__)

    def get_type_for_typeclass(self) -> ast.Name:
        """ : Dict"""
        return ast.Name(id=self.type_.__name__)
