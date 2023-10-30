from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Validator(Protocol):
    def validate(self, check_obj: Any, **kwargs) -> Any:
        pass
