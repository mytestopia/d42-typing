TEXT_SCHEMA_CODE = '''\
import string
from typing import Any, cast, TypeAlias

from d42.custom_type import CustomSchema, PathHolder, Props, ValidationResult, register_type
from d42.custom_type.utils import make_substitution_error
from d42.custom_type.visitors import Generator, Representor, Substitutor, Validator
from district42.types import StrSchema
from district42.utils import TypeOrEllipsis
from niltype import Nil, Nilable


class TextProps(Props):
    @property
    def type(self) -> StrSchema:
        return cast(StrSchema, self.get("type", StrSchema()))


class _TextSchema(CustomSchema[TextProps]):
    type: TypeAlias = StrSchema
    name = "text"
    alphabet = string.ascii_letters
    specials = " " * 5

    def __call__(self, /, value: str) -> "_TextSchema":
        str_type = self.props.type(value)
        return self.__class__(self.props.update(type=str_type))

    def len(self, /, val_or_min: TypeOrEllipsis[int],
            max: Nilable[TypeOrEllipsis[int]] = Nil) -> "_TextSchema":
        str_type = self.props.type.len(val_or_min, max)
        return self.__class__(self.props.update(type=str_type))

    def __represent__(self, visitor: Representor, indent: int = 0) -> str:
        r = f"{visitor.name}.{self.name}"
        str_type = self.props.type

        if str_type.props.value is not Nil:
            r += f"({str_type.props.value!r})"

        if str_type.props.len is not Nil:
            r += f".len({str_type.props.len!r})"
        elif (str_type.props.min_len is not Nil) and (str_type.props.max_len is not Nil):
            r += f".len({str_type.props.min_len!r}, {str_type.props.max_len!r})"
        elif str_type.props.min_len is not Nil:
            r += f".len({str_type.props.min_len!r}, ...)"
        elif str_type.props.max_len is not Nil:
            r += f".len(..., {str_type.props.max_len!r})"

        return r

    def __generate__(self, visitor: Generator) -> str:
        str_type = self.props.type

        if str_type.props.value is not Nil:
            return str_type.props.value

        if str_type.props.len is not Nil:
            length = str_type.props.len
        else:
            min_length = str_type.props.min_len if (
                str_type.props.min_len is not Nil) else 0
            max_length = str_type.props.max_len if (
                str_type.props.max_len is not Nil) else 64
            length = visitor.random.random_int(min_length, max_length)

        generated = ""
        for idx in range(length):
            alphabet = self.alphabet + self.specials
            if (idx == 0) or (idx == length - 1):
                alphabet = self.alphabet
            elif len(generated) > 0 and (generated[-1] in self.specials):
                alphabet = self.alphabet
            generated += visitor.random.random_choice(alphabet)
        return generated

    def __validate__(self, visitor: Validator, value: Any, path: PathHolder) -> ValidationResult:
        return visitor.visit_str(self.props.type, value=value, path=path)

    def __substitute__(self, visitor: Substitutor, value: Any) -> "_TextSchema":
        result = visitor.validator.visit(self, value=value)
        if result.has_errors():
            raise make_substitution_error(result, visitor.formatter)
        str_type = self.props.type % value
        return self.__class__(self.props.update(type=str_type))


TextSchema = register_type(_TextSchema.name, _TextSchema)
'''
