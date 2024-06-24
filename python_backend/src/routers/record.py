"""Router for record related operations"""

import datetime

import fastapi
from loguru import logger

import schema

router = fastapi.APIRouter()


# NOTE: Record related operations
# CRUD
# Create a new record
# Read a record
# Read a table of records
# query record
# update record
# delete record


@router.post("/record", response_model=schema.table.Record)
def create_record(record: schema.table.Record):
    """Create a new record"""
    logger.info(f"Create new record: {record}")
    return record


@router.get("/record/{table_id}", response_model=list[schema.table.Record])
def get_table(table_id: str):
    """Get a table of records"""
    logger.info(f"Get table: {table_id}")
    pass


@router.get("/record/{table_id}/query", response_model=list[schema.table.Record])
def query_record(table_id: str):
    """Query records"""
    logger.info(f"Query records")
    pass


@router.get("/record/{table_id}/{record_id}", response_model=schema.table.Record)
def get_record(table_id: str, record_id: str):
    """Get a record"""
    logger.info(f"Get record: {record_id}")
    pass


@router.put("/record/{table_id}/{record_id}", response_model=schema.table.Record)
def update_record(table_id: str, record_id: str, record: schema.table.Record):
    """Update a record"""
    logger.info(f"Update record: {record_id}")
    return record
    pass


@router.delete("/record/{table_id}/{record_id}")
def delete_record(table_id: str, record_id: str):
    """Delete a record"""
    logger.info(f"Delete record: {record_id}")
    pass
