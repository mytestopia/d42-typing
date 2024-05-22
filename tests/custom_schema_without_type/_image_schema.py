IMAGE_SCHEMA_CODE = '''\
from typing import Any

from d42.custom_type import CustomSchema, PathHolder, Props, ValidationResult, register_type
from d42.custom_type.errors import TypeValidationError, ValueValidationError
from d42.custom_type.utils import make_substitution_error
from d42.custom_type.visitors import Generator, Representor, Substitutor, Validator
from niltype import Nil

class ImageProps(Props):

    @property
    def value(self) -> Any:
        return self.get("value")

    @property
    def color(self) -> Any:
        return self.get("color")



class _ImageSchema(CustomSchema[ImageProps]):
    def __call__(self, value: str) -> "_ImageSchema":
        assert isinstance(value, str)
        return self.__class__(self.props.update(value=value))

    def color(self, value: tuple) -> "_ImageSchema":
        assert isinstance(value, tuple)
        assert self.props.color is Nil
        return self.__class__(self.props.update(color=value))

    def __represent__(self, visitor: Representor, indent: int = 0) -> str:
        r = f"{visitor.name}.image"

        if self.props.value is not Nil:
            r += f"(<binary {len(self.props.value)})"

        return r

    def __generate__(self, visitor: Generator):
        if self.props.value is not Nil:
            return self.props.value
        return 'image'

    def __validate__(self, visitor: Validator, value: Any, path: PathHolder) -> ValidationResult:
        result = visitor.make_validation_result()

        if not isinstance(value, str):
            result.add_error(TypeValidationError(path, value, str))

        if (self.props.value is not Nil) and (value != self.props.value):
            result.add_error(ValueValidationError(path, value, self.props.value))

        return result

    def __substitute__(self, visitor: Substitutor, value: Any) -> Any:
        result = visitor.validator.visit(self, value=value)
        if result.has_errors():
            raise make_substitution_error(result, visitor.formatter)

        return self.__class__(self.props.update(value=value))


ImageSchema = register_type("image", _ImageSchema)\
'''
