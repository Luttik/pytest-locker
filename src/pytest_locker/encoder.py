import json
from dataclasses import asdict, is_dataclass
from typing import Any


class DefaultLockerJsonEncoder(json.JSONEncoder):
    """Enables serialization core and Pydantic Dataclasses"""

    def default(self, obj: Any) -> Any:
        if any(
            _class.__module__ == "pydantic.main" and _class.__name__ == "BaseModel"
            for _class in type(obj).__mro__
        ):
            return obj.dict()

        if is_dataclass(obj):
            return asdict(obj)

        return obj
