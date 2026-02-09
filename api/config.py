"""Configuration for serverless functions"""
import os

# Load from environment
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
API_ID = int(os.getenv("API_ID", "964098"))
API_HASH = os.getenv("API_HASH", "3a40779521bc99b4c9753572ddd17ee7")
DATA_DIR = os.getenv("DATA_DIR", "./data")
TZ = os.getenv("TZ", "Asia/Kolkata")

# Validation
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is required")
if not API_ID or not API_HASH:
    raise ValueError("API_ID and API_HASH are required")
