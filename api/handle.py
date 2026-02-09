"""
Handle incoming Telegram updates
"""
import logging
from .telegram import Update
from .commands import process_command
from .messages import process_message, process_photo

logger = logging.getLogger(__name__)

def handle_update(update_data):
    """Process Telegram update"""
    try:
        # Parse update
        update = Update(update_data)
        
        # Handle based on type
        if update.type == "command":
            process_command(update)
        elif update.type == "text":
            process_message(update)
        elif update.type == "photo":
            process_photo(update)
        else:
            logger.warning(f"Unknown update type: {update.type}")
    
    except Exception as e:
        logger.error(f"Error handling update: {e}")
