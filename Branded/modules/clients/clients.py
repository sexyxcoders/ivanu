import os
import sys

from pyrogram import Client
from motor.motor_asyncio import AsyncIOMotorClient
from pytgcalls import PyTgCalls

from ...console import (
    API_ID,
    API_HASH,
    STRING_SESSION,
    SESSION_STRING,
    BOT_TOKEN,
    MONGO_DB_URL,
    LOG_GROUP_ID,
    LOGGER,
    SUDOERS,
)

# -------------------- Checks --------------------

def async_config():
    LOGGER.info("Checking Variables ...")

    required = {
        "API_ID": API_ID,
        "API_HASH": API_HASH,
        "BOT_TOKEN": BOT_TOKEN,
        "STRING_SESSION": STRING_SESSION,
        "MONGO_DB_URL": MONGO_DB_URL,
        "LOG_GROUP_ID": LOG_GROUP_ID,
    }

    for key, value in required.items():
        if not value:
            LOGGER.error(f"'{key}' - Not Found!")
            sys.exit(1)

    LOGGER.info("All Required Variables Collected.")


def async_dirs():
    LOGGER.info("Initializing Directories ...")

    for folder in ("downloads", "cache"):
        os.makedirs(folder, exist_ok=True)

    for file in os.listdir():
        if file.endswith((".session", ".session-journal")):
            os.remove(file)

    LOGGER.info("Directories Initialized.")


async_config()
async_dirs()

# -------------------- Clients --------------------

app = Client(
    name="BRANDEDKING82",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION,
)

assistant = None
if SESSION_STRING:
    assistant = Client(
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

# -------------------- PyTgCalls --------------------

call = PyTgCalls(assistant if assistant else app)

# -------------------- Database --------------------

mongodb = None

def init_database():
    global mongodb
    try:
        LOGGER.info("Connecting to MongoDB ...")
        client = AsyncIOMotorClient(MONGO_DB_URL)
        mongodb = client.AdityaHalder
        LOGGER.info("MongoDB Connected.")
    except Exception as e:
        LOGGER.error(f"MongoDB Connection Failed!\n{e}")
        sys.exit(1)

init_database()

# -------------------- Sudo Users --------------------

async def load_sudoers():
    sudoersdb = mongodb.sudoers
    data = await sudoersdb.find_one({"sudo": "sudo"})

    if data:
        for uid in data.get("sudoers", []):
            SUDOERS.append(int(uid))

    LOGGER.info("Sudo Users Loaded.")

# -------------------- Startup --------------------

async def run_async_clients():
    LOGGER.info("Starting Userbot ...")
    await app.start()
    LOGGER.info("Userbot Started.")

    try:
        await app.send_message(LOG_GROUP_ID, "**Userbot Started**")
    except:
        pass

    if assistant:
        LOGGER.info("Starting Assistant ...")
        await assistant.start()
        LOGGER.info("Assistant Started.")

    LOGGER.info("Starting Helper Bot ...")
    await bot.start()
    LOGGER.info("Helper Bot Started.")

    LOGGER.info("Starting PyTgCalls ...")
    await call.start()
    LOGGER.info("PyTgCalls Started.")

    await load_sudoers()