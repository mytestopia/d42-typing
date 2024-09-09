from niltype import Nil


def has_invalid_key(dictionary: dict) -> bool:
    for key in dictionary.keys():
        if not key.isidentifier():
            return True
    return False


def is_dict_without_keys(dict_value) -> bool:
    return dict_value.props.keys is Nil


def is_dict_empty(dict_value) -> bool:
    return dict_value.props.keys == {}


def is_dict_typed_as_empty(dict_value) -> bool:
    return (
            is_dict_without_keys(dict_value)
            or is_dict_empty(dict_value)
            or has_invalid_key(dict_value.props.keys)
    )
