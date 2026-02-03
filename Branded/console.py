import os
import time
import logging

from os import getenv
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler


logging.basicConfig(
    format="[%(asctime)s]:[%(levelname)s]:[%(name)s]:: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    handlers=[
        RotatingFileHandler(
            "logs.txt", maxBytes=(1024 * 1024 * 5), backupCount=10
        ),
        logging.StreamHandler(),
    ],
)

logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)


if os.path.exists("Internal"):
   load_dotenv("Internal")


API_ID = int(getenv("API_ID", "22657083"))
API_HASH = getenv("API_HASH", "d6186691704bd901bdab275ceaab88f3")
BOT_TOKEN = getenv("BOT_TOKEN", "7694271440:AAHDfhxvmOyjZmlIqZjyo7MqCFDPRW8jutI")
STRING_SESSION = getenv("STRING_SESSION", "")
MONGO_DB_URL = getenv("MONGO_DB_URL", "mongodb+srv://StarGiftBot_db_user:gld1RLm4eYbCWZlC@cluster0.erob6sp.mongodb.net/?appName=Cluster0")
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", "-1003739009228"))


# OPTIONAL VARIABLES
SESSION_STRING = getenv("SESSION_STRING", None)
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", ". !").split())



# OTHERS VARIABLES

# PM GUARD VARS
PM_GUARD = bool(getenv("PM_GUARD", True))
PM_GUARD_TEXT = getenv("PM_GUARD_TEXT", "**🥀 Hey, I am an advanced & superfast high quality userbot assistant with an upgraded version security system.\n\n🌿 I can't let you message my owner's dm without my owner's permission.\n\n🌺 My owner is offline now, please wait until my owner allows you.\n\n🍂 Please don't spam here, because spamming will force me to block you from my owner id.**")
PM_GUARD_LIMIT = int(getenv("PM_GUARD_LIMIT", 5))



# USERBOT DEFAULT IMAGE
USERBOT_PICTURE = getenv("USERBOT_PICTURE", "https://telegram.me/share/url?url=https://files.catbox.moe/9ux4mb.jpg")



# Don't Edit This Codes From This Line

LOGGER = logging.getLogger("Branded")
runtime = time.time()

FLOODXD = {}
OLD_MSG = {}
PM_LIMIT = {}
PLUGINS = {}
SUDOERS = []


COMMAND_HANDLERS = []
for x in COMMAND_PREFIXES:
    COMMAND_HANDLERS.append(x)
COMMAND_HANDLERS.append('')

