import argparse
import ast
import inspect
import logging
import os
import sys

import app.modules as modules
from app.helpers import get_module_variables, import_module, walk, get_module_imports


def main():
    ap = argparse.ArgumentParser(description='')

    ap.add_argument('-p', '--path-to-schemas', nargs='?', type=str,
                    help='name of folder in current directory containing schemas, default: schemas',
                    default='schemas')
    ap.add_argument('-v', '--verbose',
                    help='increase output verbosity',
                    action='store_true')
    ap.add_argument('-a', '--all',
                    help='generate overloads for all standard schema types',
                    action='store_true')

    args = ap.parse_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level)

    is_add_all = args.all

    cwd = os.getcwd()
    sys.path.append(cwd)

    file_count = 0
    schemas_count = 0

    blahblah_module = modules.BlahBlahModule()

    if is_add_all:
        logging.debug('.. creating standard types overload')
        blahblah_module.generate_standard_types()

    for file_name in walk(args.path_to_schemas):
        logging.debug(f'.. creating types for: {file_name}')
        module = import_module(args.path_to_schemas, file_name)
        module_source = inspect.getsource(module)
        module_ast = ast.parse(module_source)

        imports = get_module_imports(module_ast)
        logging.debug(f'.. saved imports {len(imports)} for moving to .pyi stub')
        typed_module = modules.TypedModule(file_name, imports)

        for name in get_module_variables(module_ast):
            value = getattr(module, name)

            typed_module.generate(name, value)
            blahblah_module.generate(file_name, name, value)
            schemas_count += 1

        typed_module.print()
        file_count += 1

    blahblah_module.print()

    logging.info(
        f'Successfully processed {schemas_count} schemas, {file_count} files in {args.path_to_schemas}/')

    sys.path.remove(cwd)
