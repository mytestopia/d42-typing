class FakeModuleGeneral:
    def __init__(self, stubs_folder: str):
        self.path = f'{stubs_folder}/d42/fake.py'

    def print(self):
        content = """from typing import Any

def fake(schema: Any) -> Any:
    pass
"""
        if content is not None:
            with open(f"{self.path}i", "w") as f:
                f.write(content)

