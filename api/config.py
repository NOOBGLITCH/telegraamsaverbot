"""
Configuration module for serverless webhook
Simplified for webhook-only deployment
"""

import os

# Telegram Bot Configuration
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Timezone Configuration
TIMEZONE = os.environ.get("TIMEZONE", "Asia/Kolkata")

# Metadata Fetch Configuration
METADATA_TIMEOUT = int(os.environ.get("METADATA_TIMEOUT", "5"))

# Tag Generation Configuration
MAX_TAGS = int(os.environ.get("MAX_TAGS", "8"))

# Validate required configuration
def validate_config():
    """Validate that all required configuration is present"""
    if not BOT_TOKEN:
        raise ValueError(
            "Missing required environment variable: BOT_TOKEN\n"
            "Please set BOT_TOKEN in your Vercel environment variables."
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
