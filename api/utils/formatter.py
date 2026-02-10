"""
Response formatting utilities
Optimized for Telegram Bot API HTML format
"""

from datetime import datetime
from typing import List, Optional
import pytz
from .. import config


def format_response(
    title: str,
    description: str,
    url: Optional[str],
    tags: List[str],
    timestamp: datetime
) -> str:
    """
    Format bot response with HTML
    Telegram Bot API supports HTML formatting
    
    Args:
        title: Content title
        description: Content description
        url: Original URL (or None)
        tags: List of hashtags
        timestamp: Timestamp in IST
        
    Returns:
        Formatted HTML message
    """
    # Format date and time
    date = timestamp.strftime("%d %b %Y")
    time = timestamp.strftime("%I:%M %p IST")
    
    # Tags
    tags_str = ' '.join(tags)
    u = url if url else 'N/A'
    
    # HTML formatting
    return (
        f"📌 <b>Content Saved</b>\n\n"
        f"📝 <b>Title:</b>\n{title}\n\n"
        f"📄 <b>Description:</b>\n{description}\n\n"
        f"🔗 <b>Link:</b>\n{u}\n\n"
        f"🏷️ <b>Tags:</b>\n{tags_str}\n\n"
        f"📅 <b>Date:</b> {date}\n"
        f"⏰ <b>Time:</b> {time}"
    )


def format_error_message(error_type: str) -> str:
    """Format error message using simple Markdown"""
    error_messages = {
        'no_content': '⚠️ Media received, but no readable text or link found.',
        'metadata_failed': '⚠️ Unable to fetch metadata. Showing basic information only.',
        'invalid_url': '⚠️ Invalid URL detected. Processing text only.',
    }
    
    return error_messages.get(error_type, '⚠️ An error occurred while processing your message.')


def format_media_only_message(media_type: str, timestamp: datetime) -> str:
    """Format message for media without caption"""
    emoji_map = {'photo': '🖼️', 'video': '🎥', 'audio': '🎵', 'voice': '🎤',
                 'document': '📄', 'animation': '🎬', 'sticker': '✨'}
    
    emoji = emoji_map.get(media_type.lower(), '📎')
    date = timestamp.strftime("%d %b %Y")
    time = timestamp.strftime("%I:%M %p IST")
    
    return (
        f"{emoji} <b>{media_type.capitalize()} Received</b>\n\n"
        f"ℹ️ No caption or text provided.\n\n"
        f"📅 <b>Date:</b> {date}\n"
        f"⏰ <b>Time:</b> {time}"
    )


def get_current_ist_time() -> datetime:
    """
    Get current time in IST timezone
    
    Returns:
        Current datetime in IST
    """
    tz = pytz.timezone(config.TIMEZONE)
    return datetime.now(tz)
