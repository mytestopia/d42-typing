class Typing:

    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.class_name = self.value.__class__.__name__
        self.class_type = self.value.__class__.type

    def generate_pyi(self): ...

    def generate_fake_overload(self,  path_to_schema: str): ...


class UnknownTypeSchema:

    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.class_name = self.value.__class__.__name__


class OverloadedFake:
    def __init__(self, schema_type, ast_method):
        # schema_type - тип описываемой схемы = входного параметра
        self.schema_type = schema_type
        self.ast_method = ast_method

    def __eq__(self, other):
        return self.schema_type == other.schema_type
