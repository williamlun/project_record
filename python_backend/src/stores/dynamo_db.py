"""dynamo db store"""

import json

import boto3
from boto3 import dynamodb
from boto3.dynamodb.conditions import Key, Attr

import schema

#######################
# CRUD for master table
# create user record
# read user record
# update user record
# delete user record


class DynamoClient:
    """DynamoDB client"""

    def __init__(self, table_name):
        self.table_name = table_name
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(table_name)
        self.master_table = self.dynamodb.Table("record_project_master_table")

    def _get_partition_key(self, table_name):
        """get partition key"""
        client = boto3.client("dynamodb")
        table_description = client.describe_table(TableName=table_name)
        key_schema = table_description["Table"]["KeySchema"]
        for key in key_schema:
            if key["KeyType"] == "HASH":
                partition_key_name = key["AttributeName"]
                break
        return partition_key_name

    def _query(
        self, filter_expression, key_condition_expression, expression_attribute_values
    ):
        """query dynamo"""
        response = self.table.query(
            KeyConditionExpression=key_condition_expression,
            ExpressionAttributeValues=expression_attribute_values,
        )
        return response.get("Items")

    def _get_by_id(self, _id):
        """get item from dynamo"""
        response = self.table.get_item(Key={"id": _id})
        return response.get("Item")

    def _create_user_table(self, user_id):
        """create table"""
        table = self.dynamodb.create_table(
            TableName=user_id,
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"},
                {"AttributeName": "table_id", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"},
                {"AttributeName": "table_id", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )
        table.wait_until_exists()
        return table

    def create_user(self, user_info: schema.table.UserInfo):
        """create user"""
        self._create_user_table(user_info.id)
        response = self.master_table.put_item(Item=user_info.model_dump())
        return response

    def read_user(self, user_id):
        """read user"""
        return self._get_by_id(user_id)

    def update_user(self, user_info: schema.table.UserInfo):
        """update user"""
        # TODO: update user
        pass

    def delete_user(self, user_id):
        """delete user"""
        return self.master_table.delete_item(Key={"id": user_id})

    def create_record(self, record: schema.table.Record):
        """create record"""
        response = self.table.put_item(Item=record.model_dump())
        return response

    def read_record(self, record_id):
        """read record"""
        return self._get_by_id(record_id)

    def update_record(self, record: schema.table.Record):
        """update record"""
        # TODO: update record
        pass

    def delete_record(self, record_id):
        """delete record"""
        return self.table.delete_item(Key={"id": record_id})

    def query_record(self, table_name: str, condition: dict):
        """query record"""
