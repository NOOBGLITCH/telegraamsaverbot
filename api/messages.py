"""Message handlers"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from .commands import save_content
from .telegram import send_message

def process_message(update):
    """Process text messages"""
    content = update.text
    
    # Add forward info if forwarded
    if update.forward_date:
        if update.forward_from:
            content += f"\n\nForwarded from: {update.forward_from.get('first_name', 'Unknown')}"
        elif update.forward_from_chat:
            content += f"\n\nForwarded from: {update.forward_from_chat.get('title', 'Unknown')}"
    
    save_content(update, content)

def process_photo(update):
    """Process photo messages"""
    send_message(
        update.chat_id,
        "📷 Photo received! Currently only text and URLs are supported.\nSend the photo URL or description instead."
    )
