import ast
import importlib.util
from types import ModuleType


def import_module(workdir_path: str, file_path: str) -> ModuleType:
    name = file_path[:-3].replace("/", ".")  # suffix
    spec = importlib.util.spec_from_file_location(name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_module_imports(module_ast: ast.Module) -> list[ast.ImportFrom]:
    imports = []
    for node in module_ast.body:
        if not isinstance(node, ast.ImportFrom):
            continue
        if (
                node.module not in ['d42', 'district42', 'district42_exp_types']
                and not node.module.startswith('d42.')
                and not node.module.startswith('district42.')
                and not node.module.startswith('district42_exp_types.')
                and not node.module.startswith('schemas.')
        ):
            imports.append(node)
    return imports


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
