from app.types._type import Typing
from ast_generate import annotated_assign


class ConstantTyping(Typing):

    def generate_pyi(self):
        return annotated_assign(self.name, type(self.value).__name__)
