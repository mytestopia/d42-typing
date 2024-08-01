class Typing:

    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.class_name = self.value.__class__.__name__

    def generate_pyi(self): ...

    def generate_fake_overload(self): ...


class UnknownTypeSchema:

    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.class_name = self.value.__class__.__name__
