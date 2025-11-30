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
            "messages" : 0
        }
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
