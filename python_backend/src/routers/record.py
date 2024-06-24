"""Router for record related operations"""

import datetime

import fastapi
from loguru import logger

import schema

router = fastapi.APIRouter()


# NOTE: Record related operations
# CRUD
# Create a new record


@router.post("/record", response_model=schema.table.Record)
def create_record(record: schema.table.Record):
    """Create a new record"""
    logger.info(f"Create new record: {record}")
    return record


# Read single record
# Read a table of records
# query record
# update record
# delete record
