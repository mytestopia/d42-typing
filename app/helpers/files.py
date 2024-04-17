import os
from typing import Generator


def walk(directory: str) -> Generator[str, None, None]:
    # directory += '/schemas'
    for root, _, files in os.walk(directory):
        for file in files:
            if not file.endswith(".py") or file == "__init__.py":
                continue
            yield os.path.join(root, file)
