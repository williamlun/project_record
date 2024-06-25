"""Router for record related operations"""

import pydantic

import fastapi
from loguru import logger

import schema
import service

router = fastapi.APIRouter()


# NOTE: Record related operations
# CRUD
# Create a new record
# Read a record
# Read a table of records
# query record
# update record
# delete record


@router.post("/record/{table_id}", response_model=schema.table.Record)
def create_record(record: schema.table.Record):
    """Create a new record"""
    logger.info(f"Create new record: {record}")
    response = service.record.RecordService(
        "record_project_record_table"
    ).create_record(record)
    return response


@router.get("/table/{table_id}/record", response_model=list[schema.table.Record])
def get_table(table_id: str):
    """Get a table of records"""
    logger.info(f"Get table: {table_id}")
    response = service.record.RecordService("record_project_record_table").query_record(
        table_id
    )
    return response


@router.get("/table/{table_id}/record/query", response_model=list[schema.table.Record])
def query_record(
    table_id: str,
    limit: int = 10,
    category: schema.common.RecordCategory = schema.common.RecordCategory.RECORD,
    created_after: pydantic.AwareDatetime | None = None,
    created_before: pydantic.AwareDatetime | None = None,
    record_condition: list[schema.request.FieldCondition] | None = None,
    start_key: int | None = None,
):
    """Query records"""
    logger.info(f"Query records")
    response = service.record.RecordService("record_project_record_table").query_record(
        table_id=table_id,
        limit=limit,
        category=category,
        created_after=created_after,
        created_before=created_before,
        record_condition=record_condition,
        start_key=start_key,
    )
    return response


@router.get("/table/{table_id}/record/{record_id}", response_model=schema.table.Record)
def get_record(table_id: str, record_id: str):
    """Get a record"""
    logger.info(f"Get record: {record_id}")
    response = service.record.RecordService(
        "record_project_record_table"
    ).get_record_by_id(table_id=table_id, record_id=record_id)
    return response


@router.put("/table/{table_id}/record/{record_id}", response_model=schema.table.Record)
def update_record(table_id: str, record_id: str, record: schema.table.Record):
    """Update a record"""
    logger.info(f"Update record: {record_id}")
    response = service.record.RecordService(
        "record_project_record_table"
    ).update_record(record)
    return response


@router.delete("/table/{table_id}/record/{record_id}")
def delete_record(table_id: str, record_id: str):
    """Delete a record"""
    logger.info(f"Delete record: {record_id}")
    response = service.record.RecordService(
        "record_project_record_table"
    ).delete_record(record_id)
    return response
