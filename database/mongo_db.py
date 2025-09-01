from motor.motor_asyncio import AsyncIOMotorClient

from config import DB_URI
mongo_client = AsyncIOMotorClient(DB_URI)

mongodb = mongo_client.fsub

broaddb = mongodb.broadcast

async def add_user(user_id, user):
    ssize = await broaddb.find_one({"user_id": user_id, "user": user})
    if ssize:
        await broaddb.update_one(
            {"user_id": user_id},
            {"$set": {"user": user}},
        )
    else:
        await broaddb.insert_one({"user_id": user_id, "user": user})


async def get_user(user_id):
    if r := [jo async for jo in broaddb.find({"user_id": user_id})]:
        return r
    else:
        return False


async def del_user(user_id, user):
    await broaddb.delete_one({"user_id": user_id, "user": user})
