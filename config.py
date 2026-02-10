"""
Configuration module for Telegram Content Formatter Bot
Loads environment variables and provides configuration constants
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Configuration
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Timezone Configuration
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")

# Metadata Fetch Configuration
METADATA_TIMEOUT = int(os.getenv("METADATA_TIMEOUT", "5"))

# Tag Generation Configuration
MAX_TAGS = int(os.getenv("MAX_TAGS", "8"))

# Validate required configuration
def validate_config():
    """Validate that all required configuration is present"""
    missing = []
    
    if not API_ID:
        missing.append("API_ID")
    if not API_HASH:
        missing.append("API_HASH")
    if not BOT_TOKEN:
        missing.append("BOT_TOKEN")
    
    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            "Please copy .env.example to .env and fill in the required values."
        )
    
    return True

# User-Agent for HTTP requests
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Private IP ranges to block (security)
BLOCKED_IP_PATTERNS = [
    r"^127\.",
    r"^10\.",
    r"^172\.(1[6-9]|2[0-9]|3[0-1])\.",
    r"^192\.168\.",
    r"^localhost",
]
