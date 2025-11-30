"""
For Communicating with the cosmos database
"""

# Standard Library Imports
from dotenv import load_dotenv
import os
from functools import cache

# Third Party Imports
from azure.cosmos import CosmosClient

load_dotenv()

URL = os.getenv('ACCOUNT_URI')
KEY = os.getenv('COSMOS_KEY')


@ cache
def get_cosmos_db():
    print("making the cosmos client")
    client = CosmosClient(URL, credential=KEY)
    db = client.get_database_client("spaceodyssey")
    return db.get_container_client("users")


def add_new_user(id: str, name: str):
    container = get_cosmos_db()
    container.upsert_item(
        {
            "id" : id,
            "name" : name,
            "time" : None,
            "messages" : 0,
            "last_message_time": None,
            "last_message_role": None,
            "last_agent_message": None
            
        }
    )

def get_conversation(conversation_id: str):
    container = get_cosmos_db()
    item = container.read_item(
        item=conversation_id,
        partition_key=conversation_id
    )
    return item
        

def update_message_timeout(id: str, msg_time, msg_role: str, msg: str):
    container = get_cosmos_db()
    container.patch_item(
            item=id,
            partition_key=id,
            patch_operations=[
                {"op": "replace", "path": "/last_agent_message", "value": msg},
                {"op": "replace", "path": "/last_message_role", "value": msg_role},
                {"op": "replace", "path": "/last_message_time", "value": msg_time}
            ]
    )


def update_user_messages(id: str, messages: int):
    container = get_cosmos_db()
    container.patch_item(
            item=id,
            partition_key=id,
            patch_operations=[
                {"op": "replace", "path": "/messages", "value": messages}
            ]
    )


def update_user_time(id: str, time: int):
    container = get_cosmos_db()
    container.patch_item(
            item=id,
            partition_key=id,
            patch_operations=[
                {"op": "replace", "path": "/time", "value": time}
            ]
    )


def get_all_users():
    """Fetch all users from the database"""
    container = get_cosmos_db()
    query = "SELECT * FROM c"
    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    return items
