"""schema for table related modules"""

import uuid
import datetime

import pydantic
from pydantic import Field

from schema import common

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


class BaseModel(pydantic.BaseModel):
    """base model for config"""

    model_config = pydantic.ConfigDict(
        alies_generator=to_camel,
        allow_population_by_field_name=True,
        use_enum_values=True,
    )


# For master table
class TableInfo(BaseModel):
    """schema for table information"""

    id: str = Field(default_factory=str(uuid.uuid4()))
    table_name: str
    table_owner: str
    user_edit: list[str] = []  # list of user_id
    user_read: list[str] = []  # list of user_id
    public: bool = False
    table_created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now(datetime.UTC)
    )
    table_last_edit: datetime.datetime = Field(
        default_factory=datetime.datetime.now(datetime.UTC)
    )


class UserInfo(BaseModel):
    """Schema for user information, main schema for master table

    Attributes:
        id (str): user id, partition key for dynamo db
        username (str): user name
        email (str): user email, optional
        created_at (datetime.datetime): user created time
        table (list[TableInfo]): list of table information
    """

    id: str = Field(default_factory=str(uuid.uuid4()))
    username: str
    email: str = ""
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now(datetime.UTC)
    )
    independent_table: bool = False
    table: list[TableInfo] = []


# For record table
class Record(BaseModel):
    """Schema for record items, main schema for record table

    Attributes:
        id (str): uuid for record, partition key for dynamo db
        table_id (str): table id, sort key for dynamo db
        category (RecordCategory): record category
        record_created_at (datetime.datetime): record created time
        record_updated_at (datetime.datetime): record updated time
        record (dict): record content in json format
    """

    id: str = Field(default_factory=str(uuid.uuid4()))
    table_id: str
    category: common.RecordCategory
    record_created_at: pydantic.AwareDatetime = Field(
        default_factory=datetime.datetime.now(datetime.UTC)
    )
    record_updated_at: pydantic.AwareDatetime = Field(
        default_factory=datetime.datetime.now(datetime.UTC)
    )
    record: dict = {}
