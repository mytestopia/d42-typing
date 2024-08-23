import typing
from typing import Tuple

import ast_generate
from app.helpers import get_module_to_import_from
from app.modules.module import Import
from app.types._type import OverloadedFake


class SchemaTyping:

    def __init__(self, value):
        self.value = value
        self.class_name = self.value.__name__

    def generate_fake_overload(self) -> Tuple[OverloadedFake, list[Import]]:
        imports = []

        imports.append(Import(get_module_to_import_from(self.value), self.class_name))
        imports.append(Import('typing', 'Any'))
        overload = OverloadedFake(
            typing.Any,
            ast_generate.fake_scalar_overload(self.class_name, typing.Any)
        )
        return overload, imports
