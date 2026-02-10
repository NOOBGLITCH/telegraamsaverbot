"""
Response formatting utilities
Optimized for Pyrogram's Markdown format (not MarkdownV2)
"""

from datetime import datetime
from typing import List, Optional
import pytz
import config


def format_response(
    title: str,
    description: str,
    url: Optional[str],
    tags: List[str],
    timestamp: datetime
) -> str:
    """
    Format bot response with simple Markdown
    Pyrogram only supports basic Markdown, not MarkdownV2
    
    Args:
        title: Content title
        description: Content description
        url: Original URL (or None)
        tags: List of hashtags
        timestamp: Timestamp in IST
        
    Returns:
        Formatted Markdown message
    """
    # Format date and time
    date = timestamp.strftime("%d %b %Y")
    time = timestamp.strftime("%I:%M %p IST")
    
    # Tags
    tags_str = ' '.join(tags)
    u = url if url else 'N/A'
    
    # Simple Markdown formatting (no escaping needed)
    return (
        f"📌 **Content Saved**\n\n"
        f"📝 **Title:**\n{title}\n\n"
        f"📄 **Description:**\n{description}\n\n"
        f"🔗 **Link:**\n{u}\n\n"
        f"🏷️ **Tags:**\n{tags_str}\n\n"
        f"📅 **Date:** {date}\n"
        f"⏰ **Time:** {time}"
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
        f"{emoji} **{media_type.capitalize()} Received**\n\n"
        f"ℹ️ No caption or text provided.\n\n"
        f"📅 **Date:** {date}\n"
        f"⏰ **Time:** {time}"
    )


def get_current_ist_time() -> datetime:
    """
    Get current time in IST timezone
    
    Returns:
        Current datetime in IST
    """
    tz = pytz.timezone(config.TIMEZONE)
    return datetime.now(tz)
