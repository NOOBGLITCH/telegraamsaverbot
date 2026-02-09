"""
Handle incoming Telegram updates
"""
import asyncio
import logging
from pyrogram import Client
from pyrogram.types import Update as PyrogramUpdate
from .config import API_ID, API_HASH, BOT_TOKEN
from .telegram import Update

logger = logging.getLogger(__name__)

# Bot client
bot = None

def get_bot():
    """Get or create bot client"""
    global bot
    if bot is None:
        bot = Client(
            "mindvault",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            in_memory=True  # Serverless mode
        )
    return bot

def handle_update(update_data):
    """Process Telegram update"""
    try:
        # Parse update
        update = Update(update_data)
        
        # Handle based on type
        if update.type == "command":
            asyncio.run(handle_command(update))
        elif update.type == "text":
            asyncio.run(handle_message(update))
        elif update.type == "photo":
            asyncio.run(handle_photo(update))
        else:
            logger.warning(f"Unknown update type: {update.type}")
    
    except Exception as e:
        logger.error(f"Error handling update: {e}")

async def handle_command(update):
    """Handle bot commands"""
    from .commands import process_command
    await process_command(update)

async def handle_message(update):
    """Handle text messages"""
    from .messages import process_message
    await process_message(update)

async def handle_photo(update):
    """Handle photo messages"""
    from .messages import process_photo
    await process_photo(update)
