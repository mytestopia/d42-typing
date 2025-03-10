import argparse
import ast
import inspect
import logging
import os
import sys

import app.modules as modules
from app.helpers import (
    find_d42_package,
    get_module_variables,
    import_module,
    prepare_stubs_directory,
    walk,
)


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
    ap.add_argument('-s', '--stubs-folder', nargs='?', type=str,
                    help='name of folder in current directory to create for stubs',
                    default='_stubs')
    ap.add_argument('--general-fake-stub', action='store_true',
                    help='generate general stub for fake method',
                    default=False)

    args = ap.parse_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level)

    is_add_all = args.all

    cwd = os.getcwd()
    sys.path.append(cwd)

    logging.debug(f'.. finding d42 dependency')
    d42_path = find_d42_package()
    if not d42_path:
        logging.error("Error: d42 package not found in site-packages")
        sys.exit(1)

    logging.debug(f'.. creating stubs directory {args.stubs_folder}')
    prepare_stubs_directory(args.stubs_folder, d42_path)

    file_count = 0
    schemas_count = 0
    schemas_errors_count = 0

    typed_fake_module = modules.FakeModule(args.stubs_folder) \
        if not args.general_fake_stub else modules.FakeModuleGeneral(args.stubs_folder)

    for file_name in walk(args.path_to_schemas):
        logging.debug(f'.. creating types for: {file_name}')
        module = import_module(file_name)
        module_source = inspect.getsource(module)
        module_ast = ast.parse(module_source)

        typed_schema_module = modules.TypedSchemaModule(file_name)

        for name in get_module_variables(module_ast):
            value = getattr(module, name)

            try:
                typed_schema_module.generate(name, value)
                if not args.general_fake_stub:
                    typed_fake_module.generate(file_name, name, value)
                schemas_count += 1
            except Exception:
                logging.error(f'Failed typing schema {name}, skipping')
                schemas_errors_count += 1

        typed_schema_module.print()
        file_count += 1

    if not args.general_fake_stub:
        if is_add_all:
            logging.debug('.. creating standard types overload')
            typed_fake_module.generate_standard_types()
    typed_fake_module.print()

    logging.info(
        f'Successfully processed {schemas_count} schemas, {file_count} files in {args.path_to_schemas}/')

    if schemas_errors_count:
        logging.info(
            f'Failed processed {schemas_errors_count} schemas')

    sys.path.remove(cwd)


if __name__ == '__main__':
    main()
