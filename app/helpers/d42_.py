import logging
import os
import shutil
import site
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
        init_files = [os.path.join(root, file) for file in files if file == "__init__.py"]
    return init_files

def copy_files_to_stubs(source_root: str,
                        source_files: list[str],
                        destination_root: str = "stubs"):
    for source_path in source_files:
        if not os.path.exists(source_path):
            logging.info(f"Skipping {source_path}: file does not exist")
            continue

        relative_path = str(os.path.relpath(source_path, source_root)) + "i"
        destination_path = os.path.join(destination_root, "d42", relative_path)

        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        shutil.copyfile(source_path, destination_path)
        logging.debug(f"Copied {source_path} -> {destination_path}")


def replace_fake_import():
    file_path = "stubs/d42/__init__.pyi"
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    with open(file_path, "w", encoding="utf-8") as file:
        for line in lines:
            if line.strip() == "from d42.generation import fake":
                file.write("from .fake import fake\n")
            else:
                file.write(line)