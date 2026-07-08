"""MongoDB (motor) helpers — the vault."""

from datetime import datetime, timezone

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from config import DB_NAME, MONGO_URI

_client = AsyncIOMotorClient(MONGO_URI)
_db = _client[DB_NAME]

_files = _db.files
_users = _db.users


async def save_file(user_id: int, user_name: str, folder: str,
                    file_name: str, size: int, link: str) -> str:
    doc = {
        "user_id": user_id,
        "user_name": user_name,
        "folder": folder,
        "file_name": file_name,
        "size": size,
        "link": link,
        "uploaded_at": datetime.now(timezone.utc),
    }
    result = await _files.insert_one(doc)
    return str(result.inserted_id)


async def create_folder(user_id: int, name: str) -> None:
    await _users.update_one(
        {"_id": user_id},
        {"$addToSet": {"folders": name}},
        upsert=True,
    )


async def get_folders(user_id: int) -> list:
    folders = await _files.distinct("folder", {"user_id": user_id})
    doc = await _users.find_one({"_id": user_id}) or {}
    for name in doc.get("folders", []):
        if name not in folders:
            folders.append(name)
    if "Home" not in folders:
        folders.insert(0, "Home")
    return sorted(folders, key=lambda f: (f != "Home", f.lower()))


async def get_files(user_id: int, folder: str) -> list:
    cursor = _files.find({"user_id": user_id, "folder": folder}).sort("uploaded_at", -1)
    return [doc async for doc in cursor]


async def get_file(file_id: str):
    try:
        return await _files.find_one({"_id": ObjectId(file_id)})
    except Exception:
        return None


async def delete_file(file_id: str) -> None:
    try:
        await _files.delete_one({"_id": ObjectId(file_id)})
    except Exception:
        pass


async def set_active_folder(user_id: int, folder: str) -> None:
    await _users.update_one(
        {"_id": user_id},
        {"$set": {"active_folder": folder}},
        upsert=True,
    )


async def get_active_folder(user_id: int) -> str:
    doc = await _users.find_one({"_id": user_id}) or {}
    return doc.get("active_folder", "Home")


async def get_stats(user_id: int) -> tuple:
    count = await _files.count_documents({"user_id": user_id})
    total = 0
    pipeline = [
        {"$match": {"user_id": user_id}},
        {"$group": {"_id": None, "total": {"$sum": "$size"}}},
    ]
    async for row in _files.aggregate(pipeline):
        total = row["total"]
    return count, total
