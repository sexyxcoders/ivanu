import os, sys

from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient

# ✅ NEW pytgcalls import
from pytgcalls import GroupCallFactory

from ...console import (
    API_ID,
    API_HASH,
    STRING_SESSION,
    BOT_TOKEN,
    SESSION_STRING,
    LOGGER,
    MONGO_DB_URL,
    LOG_GROUP_ID,
    SUDOERS,
)


def async_config():
    LOGGER.info("Checking Variables ...")
    if not API_ID:
        LOGGER.info("'API_ID' - Not Found !")
        sys.exit()
    if not API_HASH:
        LOGGER.info("'API_HASH' - Not Found !")
        sys.exit()
    if not BOT_TOKEN:
        LOGGER.info("'BOT_TOKEN' - Not Found !")
        sys.exit()
    if not STRING_SESSION:
        LOGGER.info("'STRING_SESSION' - Not Found !")
        sys.exit()
    if not MONGO_DB_URL:
        LOGGER.info("'MONGO_DB_URL' - Not Found !")
        sys.exit()
    if not LOG_GROUP_ID:
        LOGGER.info("'LOG_GROUP_ID' - Not Found !")
        sys.exit()
    LOGGER.info("All Required Variables Collected.")


def async_dirs():
    LOGGER.info("Initializing Directories ...")
    for d in ("downloads", "cache"):
        if d not in os.listdir():
            os.mkdir(d)

    for file in os.listdir():
        if file.endswith((".session", ".session-journal")):
            os.remove(file)

    LOGGER.info("Directories Initialized.")


async_dirs()


# -------------------- Clients --------------------

app = Client(
    name="BRANDEDKING82",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION,
)

ass = Client(
    name="BRANDEDKING82_ASS",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
)

bot = Client(
    name="BRANDEDKING82_BOT",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# -------------------- PyTgCalls (FIXED) --------------------

if not SESSION_STRING:
    group_call_factory = GroupCallFactory(app)
else:
    group_call_factory = GroupCallFactory(ass)

call = group_call_factory.get_group_call()


# -------------------- Database --------------------

def mongodbase():
    global mongodb
    try:
        LOGGER.info("Connecting To Your Database ...")
        async_client = AsyncIOMotorClient(MONGO_DB_URL)
        mongodb = async_client.AdityaHalder
        LOGGER.info("Connected To Your Database.")
    except Exception as e:
        LOGGER.error(f"Failed To Connect Database!\nError: {e}")
        sys.exit()


mongodbase()


async def sudo_users():
    sudoersdb = mongodb.sudoers
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = [] if not sudoers else sudoers["sudoers"]

    for user_id in sudoers:
        SUDOERS.append(int(user_id))

    LOGGER.info("Sudo Users Loaded.")


# -------------------- Startup --------------------

async def run_async_clients():
    LOGGER.info("Starting Userbot ...")
    await app.start()
    LOGGER.info("Userbot Started.")

    try:
        await app.send_message(LOG_GROUP_ID, "**Userbot Started.**")
    except:
        pass

    if SESSION_STRING:
        LOGGER.info("Starting Assistant ...")
        await ass.start()
        LOGGER.info("Assistant Started.")

    LOGGER.info("Starting Helper Robot ...")
    await bot.start()
    LOGGER.info("Helper Robot Started.")

    LOGGER.info("Starting PyTgCalls Client ...")
    await call.start()
    LOGGER.info("PyTgCalls Client Started.")

    await sudo_users()