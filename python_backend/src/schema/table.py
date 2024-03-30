"""schema for table related modules"""

import uuid
import enum
import datetime

import pydantic
from pydantic import Field

################################################
# There are one master table in the dynamo db, which stores all user information and their table information
# Each use will have a table to store their records, the table name will be the user id
# The record will be stored in the user's table, and the record will have a category to indicate the type of the record
# The table in user's side is a virtual table, the record will stores their table information
################################################


def to_camel(string: str) -> str:
    splitted_string = string.split("_")
    return splitted_string[0] + "".join(
        word.capitalize() for word in splitted_string[1:]
    )


class RecordCategory(enum.Enum):
    """record category"""

    RECORD = "record"
    TEMPLATE = "template"
    INFORMATION = "information"
    REMARK = "remark"


# For master table
class TableInfo(pydantic.BaseModel):
    """schema for table information"""

    model_config = pydantic.ConfigDict(alies_generator=to_camel)

    id: str = Field(default_factory=str(uuid.uuid4()))
    table_name: str
    table_owner: str
    user_edit: list[str] = []  # list of user_id
    user_read: list[str] = []  # list of user_id
    public: bool = False
    table_created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now(datetime.UTC)
    )


class UserInfo(pydantic.BaseModel):
    """schema for user information"""

    model_config = pydantic.ConfigDict(alies_generator=to_camel)

    id: str = Field(default_factory=str(uuid.uuid4()))
    username: str
    email: str = ""
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    table: list[TableInfo] = []


# For record table
class Record(pydantic.BaseModel):
    """schema for record"""

    model_config = pydantic.ConfigDict(alies_generator=to_camel, extra="allow")

    id: str = Field(default_factory=str(uuid.uuid4()))
    table_id: str
    category: str
    record_created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now(datetime.UTC)
    )
    record_updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now(datetime.UTC)
    )
    record: dict = {}
