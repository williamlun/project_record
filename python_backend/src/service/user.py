"""User related services"""

import schema
import stores


class UserService:
    """User related services"""

    def __init__(self, table_name: str):
        self.db_client = stores.dynamo_db.DynamoClient(table_name)

    def create_user(self, user_info: schema.table.UserInfo):
        """create user"""
        response = self.db_client.create_item(item=user_info.model_dump())
        return response

    def get_user_by_id(self, user_id: str) -> schema.table.UserInfo:
        """read user"""
        response = self.db_client.get_by_id(user_id)
        # TODO: convert response to schema
        return response

    def update_user(self, user_info: schema.table.UserInfo) -> schema.table.UserInfo:
        """update user"""
        user_id = user_info.pop("id")
        username = user_info.pop("username")
        response = self.db_client.update_item(
            partition_key_value=user_id,
            sort_key_value=username,
            updates=user_info,
        )
        # TODO: convert response to schema
        return response

    def delete_user_by_id(self, user_id: str):
        """delete user"""
        return self.db_client.delete_item(partition_key_value=user_id)

    def get_user_tables(self, user_id: str) -> list[schema.table.TableInfo]:
        """get user tables"""

        user_info = self.get_user_by_id(user_id)
        return user_info.get("table", [])
