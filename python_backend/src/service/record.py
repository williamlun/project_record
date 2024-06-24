"""Record related services"""

import datetime
import pydantic
import schema
import stores

from boto3.dynamodb.conditions import Attr, Key


class RecordService:
    """Record related services"""

    def __init__(self, table_name: str):
        self.db_client = stores.dynamo_db.DynamoClient(table_name)

    def create_record(self, record: schema.table.Record):
        """create record"""
        response = self.db_client.create_item(item=record.model_dump())
        return response

    def get_record_by_id(self, record_id):
        """read record"""
        return self.db_client.get_by_id(record_id)

    def update_record(self, record: schema.table.Record) -> schema.table.Record:
        """update record"""
        record_id = record.pop("id")
        response = self.db_client.update_item(
            partition_key_value=record_id, updates=record
        )
        # TODO: convert response to schema
        return response

    def delete_record(self, record_id):
        """delete record"""
        return self.db_client.delete_item(partition_key_value=record_id)

    def _generate_filter_expression(
        self,
        category: schema.common.RecordCategory = schema.common.RecordCategory.RECORD,
        created_after: pydantic.AwareDatetime | None = None,
        created_before: pydantic.AwareDatetime | None = None,
        record_condition: list[schema.request.FieldCondition] | None = None,
    ) -> str:
        filter_expressions = []
        filter_expressions.append(Attr("category").eq(category))
        if created_after & created_before:
            filter_expressions.append(
                Attr("record_created_at").between(
                    created_after.timestamp, created_before.timestamp
                )
            )
        elif created_after:
            filter_expressions.append(
                Attr("record_created_at").gt(created_after.timestamp)
            )
        elif created_before:
            filter_expressions.append(
                Attr("record_created_at").lt(created_before.timestamp)
            )
        if record_condition:
            for field in record_condition:
                field_name = "record." + field.field
                if field.operation == schema.common.Operator.EQ:
                    filter_expressions.append(Attr(field_name).eq(field.value))
                elif field.operation == schema.common.Operator.NE:
                    filter_expressions.append(Attr(field_name).ne(field.value))
                elif field.operation == schema.common.Operator.GT:
                    filter_expressions.append(Attr(field_name).gt(field.value))
                elif field.operation == schema.common.Operator.GTE:
                    filter_expressions.append(Attr(field_name).gte(field.value))
                elif field.operation == schema.common.Operator.LT:
                    filter_expressions.append(Attr(field_name).lt(field.value))
                elif field.operation == schema.common.Operator.LTE:
                    filter_expressions.append(Attr(field_name).lte(field.value))
                elif field.operation == schema.common.Operator.EXISTS:
                    filter_expressions.append(Attr(field_name).exists())
                elif field.operation == schema.common.Operator.NOT_EXISTS:
                    filter_expressions.append(Attr(field_name).not_exists())
                elif field.operation == schema.common.Operator.CONTAINS:
                    filter_expressions.append(Attr(field_name).contains(field.value))
                elif field.operation == schema.common.Operator.IS_IN:
                    filter_expressions.append(Attr(field_name).is_in(field.value))
                elif field.operation == schema.common.Operator.BEGINS_WITH:
                    filter_expressions.append(Attr(field_name).begins_with(field.value))
            filter_expression = filter_expressions[0]
            for expr in filter_expressions[1:]:
                filter_expression = filter_expression & expr
        return filter_expression

    def get_query_result_count(
        self,
        table_id: str,
        category: schema.common.RecordCategory = schema.common.RecordCategory.RECORD,
        created_after: pydantic.AwareDatetime | None = None,
        created_before: pydantic.AwareDatetime | None = None,
        record_condition: list[schema.request.FieldCondition] | None = None,
    ):
        """get query result count"""
        filter_expression = self._generate_filter_expression(
            category=category,
            created_after=created_after,
            created_before=created_before,
            record_condition=record_condition,
        )
        key_condition = Key("sort_key").eq(table_id)
        response = self.db_client.query_count(
            key_condition_expression=key_condition, filter_expression=filter_expression
        )
        return response

    def query_record(
        self,
        table_id: str,
        limit: int = 10,
        category: schema.common.RecordCategory = schema.common.RecordCategory.RECORD,
        created_after: pydantic.AwareDatetime | None = None,
        created_before: pydantic.AwareDatetime | None = None,
        record_condition: list[schema.request.FieldCondition] | None = None,
        start_key: int | None = None,
    ):
        """query record"""
        key_condition = Key("sort_key").eq(table_id)
        filter_expression = self._generate_filter_expression(
            category=category,
            created_after=created_after,
            created_before=created_before,
            record_condition=record_condition,
        )

        response = self.db_client.query(
            key_condition_expression=key_condition,
            filter_expression=filter_expression,
            limit=limit,
            start_key=start_key,
        )
        # TODO: convert response to schema
        return response
