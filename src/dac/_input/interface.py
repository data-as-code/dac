from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Validator(Protocol):
    @classmethod
    def validate(cls, check_obj: Any, **kwargs) -> Any:
        pass
