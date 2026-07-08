"""Configuration — everything comes from environment variables.

NEVER hardcode your bot token here. If your token ever leaks
(e.g. pasted in a chat or pushed to GitHub), revoke it immediately
via @BotFather -> /revoke and set the new one in your environment.
"""

import os

# Telegram MTProto credentials — get these free from https://my.telegram.org
# (Pyrogram needs them even for bots; the client will not start without them.)
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# MongoDB — the vault
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "FileUploader")

# Backup / log group where every upload is mirrored (bot must be admin there)
LOG_GROUP_ID = int(os.environ.get("LOG_GROUP_ID", "-1004413449396"))

# Optional Gofile account token (premium accounts unlock true direct links)
GOFILE_TOKEN = os.environ.get("GOFILE_TOKEN", "")

# Direct image link shown on /start and about (ibb.co direct link, etc.)
START_IMG = os.environ.get("START_IMG", "https://ibb.co/your-direct-image-link")

# Local scratch directory for downloads before they go to Gofile
DOWNLOAD_DIR = "downloads"
