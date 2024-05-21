import ast


class Import:
    def __init__(self, module, item):
        self.module = module
        self.item = item

    def __eq__(self, other):
        return self.module == other.module and self.item == other.item

    def __repr__(self):
        return f'from {self.module} import {self.item}'

    def to_ast(self):
        return ast.ImportFrom(module=self.module, names=[ast.alias(name=self.item, asname=None)], level=0)


class Module:
    imports: list

    def __init__(self, path: str):
        self.path = path
        self.imports = []
        self.typed_items = []

    def add_import(self, module, *imported_items):
        # todo squash imports
        for item in imported_items:
            new_import = Import(module, item)
            if new_import not in self.imports:
                self.imports.append(new_import)

    def get_ast_content(self) -> list:
        return []

    def get_printable_content(self) -> str | None:
        module = ast.Module(body=self.get_ast_content(), type_ignores=[])
        if module.body is None:
            return None
        return ast.unparse(ast.fix_missing_locations(module))  # Python 3.9+

    def print(self):
        content = self.get_printable_content()
        if content is not None:
            with open(f"{self.path}i", "w") as f:
                f.write(content)
