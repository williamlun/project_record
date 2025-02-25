"""Schema for request body"""

from typing import Any

import pydantic
from schema import common


def to_camel(string: str) -> str:
    splitted_string = string.split("_")
    return splitted_string[0] + "".join(
        word.capitalize() for word in splitted_string[1:]
    )


class BaseModel(pydantic.BaseModel):
    """base model for config"""

    model_config = pydantic.ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        use_enum_values=True,
    )


class FieldCondition(BaseModel):
    """Schema for field condition"""

    field: str
    field_type: common.FieldType
    operation: common.Operator
    value: Any = None
