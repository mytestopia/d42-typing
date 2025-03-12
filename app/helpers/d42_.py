import logging
import os
import shutil
import site
import sys
from typing import Optional

logger = logging.getLogger(__name__)


def find_d42_package() -> Optional[str]:
    for path in site.getsitepackages() + [site.getusersitepackages()]:
        d42_path = os.path.join(path, "d42")
        if os.path.exists(d42_path):
            return d42_path
    return None


def list_init_files(d42_path: str):
    init_files = []
    for root, _, files in os.walk(d42_path):
        for file in files:
            if file == "__init__.py":
                init_files.append(os.path.join(root, file))
    return init_files

def copy_files_to_stubs(source_root: str,
                        source_files: list[str],
                        destination_root: str):
    for source_path in source_files:
        if not os.path.exists(source_path):
            logging.info(f"Skipping {source_path}: file does not exist")
            continue

        relative_path = str(os.path.relpath(source_path, source_root)) + "i"
        destination_path = os.path.join(destination_root, "d42", relative_path)

        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        shutil.copyfile(source_path, destination_path)
        logging.debug(f"... copied {destination_path}")


def replace_fake_import(stubs_folder: str):
    file_path = f"{stubs_folder}/d42/__init__.pyi"
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    with open(file_path, "w", encoding="utf-8") as file:
        for line in lines:
            if line.strip() == "from d42.generation import fake":
                file.write("from .fake import fake\n")
            else:
                file.write(line)


def prepare_stubs_directory(stubs_folder: str, d42_path: str):
    source_files = list_init_files(d42_path)
    copy_files_to_stubs(d42_path, source_files, destination_root=stubs_folder)
    replace_fake_import(stubs_folder)
