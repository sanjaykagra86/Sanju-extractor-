import os
from os import getenv
# ---------------R---------------------------------
API_ID = int(os.environ.get("API_ID", "24495656"))
# ------------------------------------------------
API_HASH = os.environ.get("API_HASH", "61afcf68c6429714dd18acd07f246571")
# ----------------D--------------------------------
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8045368746:AAHZwlpzvg-H2uzJXKfYzJt2SZ5bbabV0BA")
# -----------------A-------------------------------
BOT_USERNAME = os.environ.get("BOT_USERNAME")
# ------------------X------------------------------
OWNER_ID = int(os.environ.get("OWNER_ID", "5548106944"))
# ------------------X------------------------------

SUDO_USERS = list(map(int, getenv("SUDO_USERS", "5548106944").split()))
# ------------------------------------------------
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002410271415"))
# ------------------------------------------------
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://nicenice:EwJT5zWkfBkrWXFP@cluster0.gcn92.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# -----------------------------------------------
PREMIUM_LOGS = int(os.environ.get("PREMIUM_LOGS", "-1002410271415"))
