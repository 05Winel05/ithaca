"""Verify Atlas connectivity and basic write/read/delete permissions."""

from datetime import datetime, timezone
from uuid import uuid4

from dotenv import load_dotenv
from database import get_database

load_dotenv()


def main():
    try:
        db = get_database()
        if db is None:
            print("MongoDB is not configured. Add MONGODB_URI to your .env file.")
            return 1
        token = str(uuid4())
        collection = db["connection_checks"]
        collection.insert_one({"_id": token, "created_at": datetime.now(timezone.utc)})
        found = collection.find_one({"_id": token})
        collection.delete_one({"_id": token})
        if not found:
            print("Connected, but the read test failed. Check database permissions.")
            return 1
        print("MongoDB Atlas connection OK. Read, write, and delete all succeeded.")
        print("Database:", db.name)
        return 0
    except Exception as exc:
        print("MongoDB connection failed:", type(exc).__name__)
        print("Check the Atlas IP access list, database username/password, connection string, and network connection.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
