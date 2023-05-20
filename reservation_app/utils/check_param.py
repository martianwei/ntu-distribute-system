from typing import Generic, TypeVar

T = TypeVar('T')


class MyGeneric(Generic[T]):
    pass


def check_parameter(param, name, expected_type):
    if not isinstance(param, MyGeneric[expected_type]):
        raise TypeError(
            f"Parameter '{name}' should be of type {expected_type.__name__}, but received {type(param).__name__}")
