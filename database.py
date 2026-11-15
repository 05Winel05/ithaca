"""MongoDB Atlas connection for the Ithaca study planner."""

import os
from functools import lru_cache


def is_configured():
    uri = os.environ.get("MONGODB_URI", "").strip()
    return uri.startswith("mongodb://") or uri.startswith("mongodb+srv://")


@lru_cache(maxsize=1)
def get_client():
    from pymongo import MongoClient
    from pymongo.server_api import ServerApi

    uri = os.environ.get("MONGODB_URI", "").strip()
    return MongoClient(uri, server_api=ServerApi("1"), serverSelectionTimeoutMS=4000)


def get_database():
    if not is_configured():
        return None
    client = get_client()
    client.admin.command("ping")
    name = os.environ.get("MONGODB_DB", "ithaca").strip() or "ithaca"
    return client[name]
