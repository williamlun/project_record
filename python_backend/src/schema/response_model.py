"""Response model for the API"""

import datetime
import pydantic


from schema import common, table


def to_camel(string: str) -> str:
    splitted_string = string.split("_")
    return splitted_string[0] + "".join(
        word.capitalize() for word in splitted_string[1:]
    )


class BaseResponseModel(pydantic.BaseModel):
    """Base Model of all response"""

    model_config = pydantic.ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        use_enum_values=True,
    )


class SimpleTableInfo(BaseResponseModel):
    """Schema for simple table information"""

    id: str
    table_name: str


class UserInfo(BaseResponseModel):
    """Schema for user information"""

    id: str
    username: str
    email: str
    created_at: datetime.datetime
    independent_table: bool
    table: list[SimpleTableInfo]


class FullTableInfo(SimpleTableInfo):
    """Full table information"""

    table_owner: str
    user_edit: list[str]
    user_read: list[str]
    public: bool
    table_created_at: datetime.datetime
    table_last_edit: datetime.datetime


class RecordQuery(BaseResponseModel):
    """Schema for record query response"""

    category: common.RecordCategory
    record_count: int
    records: list[table.Record]
