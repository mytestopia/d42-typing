import argparse
import ast
import inspect
import os
import sys


import app.modules as modules
from app.helpers import get_module_variables, import_module, walk


def main():
    blahblah_module = modules.BlahBlahModule()

    ap = argparse.ArgumentParser(description='')

    ap.add_argument('-p', '--path-to-schemas', nargs='?', type=str, help='path to schemas')
    args = ap.parse_args()
    args_dict = dict()
    for key in vars(args):
        value = getattr(args, key)
        args_dict[key] = value

    path = args_dict['path_to_schemas']

    cwd = os.getcwd()
    sys.path.append(cwd)

    for file_name in walk(path):
        print(f'creating types for: {file_name}')
        module = import_module(path, file_name)
        module_source = inspect.getsource(module)
        module_ast = ast.parse(module_source)

        typed_module = modules.TypedModule(file_name)

        for name in get_module_variables(module_ast):
            value = getattr(module, name)

            typed_module.generate(name, value)
            blahblah_module.generate(file_name, name, value)

        typed_module.print()
        # break

    blahblah_module.print()

    sys.path.remove(cwd)

main()
