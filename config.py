import os
from os import getenv
# ---------------R---------------------------------
API_ID = int(os.environ.get("API_ID", "23701738"))
# ------------------------------------------------
API_HASH = os.environ.get("API_HASH", "28f54cde54548df7354035c038ab3ddd")
# ----------------D--------------------------------
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7130342243:AAHGQ0sTu9SLiJJ58Q7XD5B0v4RF88pZfAI")
# -----------------A-------------------------------
BOT_USERNAME = os.environ.get("BOT_USERNAME")
# ------------------X------------------------------
OWNER_ID = int(os.environ.get("OWNER_ID", "1376801961"))
# ------------------X------------------------------

SUDO_USERS = list(map(int, getenv("SUDO_USERS", "1376801961").split()))
# ------------------------------------------------
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002091954872"))
# ------------------------------------------------
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://nicenice:EwJT5zWkfBkrWXFP@cluster0.gcn92.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# -----------------------------------------------
PREMIUM_LOGS = int(os.environ.get("PREMIUM_LOGS", "-1002297983649"))
