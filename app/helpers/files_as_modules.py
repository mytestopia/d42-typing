import ast
import importlib.util
from types import ModuleType
from typing import Dict, List


def import_module(workdir_path: str, file_path: str) -> ModuleType:
    name = file_path[:-3].replace("/", ".")  # suffix
    spec = importlib.util.spec_from_file_location(name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_module_imports(module_ast: ast.Module) -> Dict[str, Dict[str, str | None]]:
    imports = {}
    for node in module_ast.body:
        if not isinstance(node, ast.ImportFrom):
            continue
        for name in node.names:
            real_name = name.asname if name.asname else name.name
            imports[real_name] = {
                "name": name.name,
                "module": node.module,
                "alias": name.asname,
            }
    return imports


def get_module_variables(module_ast: ast.Module) -> List[str]:
    variables = []
    for node in module_ast.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            assert isinstance(target, ast.Name)
            if target.id.startswith("__"):
                continue
            variables.append(target.id)
    return variables


def load_module_from_string(module_name, module_content):
    spec = importlib.util.spec_from_loader(module_name, loader=None, origin='string')

    module = importlib.util.module_from_spec(spec)

    exec(module_content, module.__dict__)
    return module
