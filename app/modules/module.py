import ast
import logging


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

    def no_import_duplicates(self, import_: Import) -> bool:
        return import_ not in self.imports

    def duplicate_in_module(self, import_: Import):
        if import_.item in [i.item for i in self.imports]:
            return import_.module
        return None

    def add_import(self, module, *imported_items):
        # todo squash imports
        for item in imported_items:
            new_import = Import(module, item)
            if self.no_import_duplicates(new_import):

                duplicate_module = self.duplicate_in_module(new_import)
                if duplicate_module:
                    logging.warning(f'Item {new_import.item} has already imported from module {duplicate_module}')

                self.imports.append(new_import)

    def add_import_new(self, *imports):
        for import_ in imports:
            if self.no_import_duplicates(import_):

                duplicate_module = self.duplicate_in_module(import_)
                if duplicate_module:
                    logging.warning(f'Item {import_.item} has already imported from module {duplicate_module}')

                self.imports.append(import_)

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
