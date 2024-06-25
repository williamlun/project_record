"""dynamo db store"""

import json

import boto3
from boto3 import dynamodb
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from loguru import logger

import schema

#######################
# CRUD for master table
# create user record
# read user record
# update user record
# delete user record


def handle_client_error(func):
    """handle client error"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ClientError, BaseException) as e:  # pylint: disable=broad-except
            logger.error(e)
            raise e

    return wrapper


class DynamoClient:
    """DynamoDB client"""

    def __init__(self, table_name: str):
        self.table_name = table_name
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(table_name)

    def _get_partition_key(self, table_name: str):
        """get partition key"""
        client = boto3.client("dynamodb")
        table_description = client.describe_table(TableName=table_name)
        key_schema = table_description["Table"]["KeySchema"]
        for key in key_schema:
            if key["KeyType"] == "HASH":
                partition_key_name = key["AttributeName"]
                break
        return partition_key_name

    def _get_sort_key(self, table_name: str):
        """get sort key"""
        client = boto3.client("dynamodb")
        table_description = client.describe_table(TableName=table_name)
        key_schema = table_description["Table"]["KeySchema"]
        for key in key_schema:
            if key["KeyType"] == "RANGE":
                sort_key_name = key["AttributeName"]
                break
        return sort_key_name

    def _create_table(self, user_id):
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

    @handle_client_error
    def query(self, filter_expression, key_condition_expression, limit, start_key):
        """query dynamo"""
        response = self.table.query(
            KeyConditionExpression=key_condition_expression,
            FilterExpression=filter_expression,
            limit=limit,
            ExclusiveStartKey=start_key,
        )
        return response.get("Items")

    def query_count(self, filter_expression, key_condition_expression):
        """query dynamo"""
        response = self.table.query(
            KeyConditionExpression=key_condition_expression,
            FilterExpression=filter_expression,
            setSelect="COUNT",
        )
        return response.get("Count")

    @handle_client_error
    def get_by_id(self, partition_key_value: str, sort_key_value: str):
        """get item from dynamo"""
        partition_key = self._get_partition_key(self.table_name)
        sort_key = self._get_sort_key(self.table_name)
        response = self.table.get_item(
            Key={partition_key: partition_key_value, sort_key: sort_key_value}
        )
        return response.get("Item")

    @handle_client_error
    def create_item(self, item: dict):
        """create new item"""
        response = self.table.put_item(Item=item)
        return response

    @handle_client_error
    def update_item(self, partition_key_value, sort_key_value=None, updates=None):
        """update item"""

        # Construct the key for the item to update
        key = {"partition_key": partition_key_value}
        if sort_key_value:
            key["sort_key"] = sort_key_value
        # Construct the UpdateExpression and ExpressionAttributeValues
        update_expression_parts = []
        expression_attribute_values = {}

        for attr, value in updates.items():
            update_expression_parts.append(f"{attr} = :{attr}")
            expression_attribute_values[f":{attr}"] = value

        update_expression = "SET " + ", ".join(update_expression_parts)

        # Perform the update operation
        response = self.table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW",  # Return the updated attributes
        )

        # Process the response
        updated_attributes = response.get("Attributes", {})
        return updated_attributes

    @handle_client_error
    def delete_item(self, partition_key_value, sort_key_value=None):
        """delete item"""
        # Construct the key for the item to delete
        key = {"partition_key": partition_key_value}
        if sort_key_value:
            key["sort_key"] = sort_key_value

        # Perform the delete operation
        response = self.table.delete_item(Key=key)

        return response
