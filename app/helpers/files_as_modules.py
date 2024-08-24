import ast
import importlib.util
from types import ModuleType


def import_module(file_path: str) -> ModuleType:
    name = file_path[:-3].replace("/", ".")
    spec = importlib.util.spec_from_file_location(name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_module_variables(module_ast: ast.Module) -> list[str]:
    variables = []

    def process_target(target: ast.expr):
        assert isinstance(target, ast.Name)
        if target.id.startswith("__"):
            return
        variables.append(target.id)

    for node in module_ast.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                process_target(target)
        elif isinstance(node, ast.AnnAssign):
            process_target(node.target)
    return variables


def load_module_from_string(module_name, module_content):
    spec = importlib.util.spec_from_loader(module_name, loader=None, origin='string')

    module = importlib.util.module_from_spec(spec)

    exec(module_content, module.__dict__)
    return module
