"""Configuration module"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram credentials
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
API_ID = int(os.getenv("API_ID", "964098"))
API_HASH = os.getenv("API_HASH", "3a40779521bc99b4c9753572ddd17ee7")

# Storage
DATA_DIR = os.getenv("DATA_DIR", "./data")

# Validation
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is required")
if not API_ID or not API_HASH:
    raise ValueError("API_ID and API_HASH are required")

# Ensure directories exist
os.makedirs(f"{DATA_DIR}/items", exist_ok=True)
os.makedirs(f"{DATA_DIR}/users", exist_ok=True)
os.makedirs(f"{DATA_DIR}/exports", exist_ok=True)
os.makedirs("./sessions", exist_ok=True)