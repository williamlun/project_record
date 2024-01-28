"""schema for table related modules"""

import uuid
import datetime

import pydantic
from pydantic import Field


def to_camel(string: str) -> str:
    splitted_string = string.split("_")
    return splitted_string[0] + "".join(
        word.capitalize() for word in splitted_string[1:]
    )


class TableInfo(pydantic.BaseModel):
    """schema for table information"""

    model_config = pydantic.ConfigDict(alies_generator=to_camel)

    table_id: str = Field(default_factory=str(uuid.uuid4()))
    table_name: str
    user_edit: list[str] = []  # list of user_id
    user_read: list[str] = []  # list of user_id
    public: bool = False
    table_created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow
    )


class UserInfo(pydantic.BaseModel):
    """schema for user information"""

    model_config = pydantic.ConfigDict(alies_generator=to_camel)

    user_id: str = Field(default_factory=str(uuid.uuid4()))
    user_name: str
    user_email: str = ""
    user_created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    table_info: list[TableInfo] = []


class Record(pydantic.BaseModel):
    """schema for record"""

    model_config = pydantic.ConfigDict(alies_generator=to_camel, extra="allow")

    record_id: str = Field(default_factory=str(uuid.uuid4()))
    table_id: str
    record_created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow
    )
    record_updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow
    )
