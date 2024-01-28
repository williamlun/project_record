"""dynamo db store"""
import json

import boto3
from boto3 import dynamodb
from boto3.dynamodb.conditions import Key, Attr


class DynamoClient:
    """DynamoDB client"""

    def __init__(self, table_name):
        self.table_name = table_name
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(table_name)

    def get(self, key):
        """get item from dynamo"""
        response = self.table.get_item(Key=key)
        return response.get("Item")

    def put(self, item):
        """put item to dynamo"""
        self.table.put_item(Item=item)

    def query(self, key_condition_expression, expression_attribute_values):
        """query dynamo"""
        response = self.table.query(
            KeyConditionExpression=key_condition_expression,
            ExpressionAttributeValues=expression_attribute_values,
        )
        return response.get("Items")
