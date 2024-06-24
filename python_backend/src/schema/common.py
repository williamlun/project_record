"""Common schema for record project"""

import enum


class Operator(enum.StrEnum):
    """operator for query"""

    EQ = "EQ"
    NE = "NE"
    GT = "GT"
    GTE = "GTE"
    LT = "LT"
    LTE = "LTE"
    EXISTS = "EXISTS"
    NOT_EXISTS = "NOT_EXISTS"
    CONTAINS = "CONTAINS"
    IS_IN = "IS_IN"
    BEGINS_WITH = "BEGINS_WITH"


class FieldType(enum.StrEnum):
    """field type"""

    STRING = "STRING"
    NUMBER = "NUMBER"
    BOOLEAN = "BOOLEAN"
    LIST = "LIST"
    MAP = "MAP"


class RecordCategory(enum.StrEnum):
    """record category"""

    RECORD = "RECORD"
    TEMPLATE = "TEMPLATE"
    INFORMATION = "INFORMATION"
    REMARK = "REMARK"
