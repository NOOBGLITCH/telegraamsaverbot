"""Configuration for serverless functions"""
import os

# Load from environment - ONLY BOT_TOKEN needed for Bot API
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
DATA_DIR = os.getenv("DATA_DIR", "./data")
TZ = os.getenv("TZ", "Asia/Kolkata")

# Validation
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is required")
