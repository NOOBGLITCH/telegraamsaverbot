"""
Telegram Instant Content Formatter Bot
A stateless bot that processes messages, extracts metadata, and formats content instantly

Framework: Pyrogram
Architecture: Stateless (no database, no persistent storage)
"""

import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode

import config
from utils import (
    get_first_valid_url,
    fetch_metadata,
    generate_tags,
    format_response,
    format_error_message,
    format_media_only_message,
    get_current_ist_time
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Validate configuration
config.validate_config()

# Initialize Pyrogram client
app = Client(
    "content_formatter_bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)


@app.on_message(filters.private & ~filters.command(['start', 'help']))
async def handle_message(client: Client, message: Message):
    """
    Main message handler - processes all incoming messages
    Stateless: processes and forgets immediately after reply
    
    Args:
        client: Pyrogram client
        message: Incoming message
    """
    try:
        # Get current timestamp (IST)
        timestamp = get_current_ist_time()
        
        # Extract text content (from message or caption)
        text_content = message.text or message.caption or ''
        
        # Detect media type
        media_type = _get_media_type(message)
        
        # If no text and no media, skip
        if not text_content and not media_type:
            return
        
        # Extract URL from text
        url = get_first_valid_url(text_content)
        
        # Initialize metadata
        title = 'Untitled Content'
        description = 'No description available'
        
        # Fetch metadata if URL exists
        if url:
            try:
                metadata = await fetch_metadata(url)
                title = metadata.get('title', title)
                description = metadata.get('description', description)
            except Exception as e:
                logger.warning(f"Metadata fetch failed: {e}")
                # Continue with fallback values
        
        # If no URL and no meaningful text, handle media-only case
        if not url and not text_content.strip():
            if media_type:
                response = format_media_only_message(media_type, timestamp)
                await message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
            return
        
        # Use text as title if no URL metadata
        if not url and text_content.strip():
            # Use first 100 chars as title
            title = text_content[:100].strip()
            if len(text_content) > 100:
                title += '...'
            # Use full text as description
            description = text_content.strip()
        
        # Generate tags
        tags = generate_tags(
            title=title,
            description=description,
            caption=text_content,
            media_type=media_type,
            url=url
        )
        
        # Format response
        response = format_response(
            title=title,
            description=description,
            url=url,
            tags=tags,
            timestamp=timestamp
        )
        
        # Send reply
        await message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
        
        # Log processing (no data stored)
        logger.info(f"Processed message from user {message.from_user.id}")
        
        # Memory is automatically cleared (stateless design)
        
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        error_msg = format_error_message('general')
        await message.reply_text(error_msg, parse_mode=ParseMode.MARKDOWN)


@app.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    """Handle /start command"""
    welcome_message = """
👋 **Welcome to Content Formatter Bot!**

I'm a stateless bot that instantly formats any content you send me.

**What I do:**
✅ Extract metadata from URLs
✅ Generate automatic tags
✅ Format content beautifully
✅ Add IST timestamps

**What I support:**
📝 Text messages
🔗 URLs and links
🖼️ Photos with captions
🎥 Videos with captions
🎵 Audio with captions
📄 Documents with captions

**Privacy:**
🔒 No data storage
🔒 No user tracking
🔒 Instant processing and forgetting

Just send me anything, and I'll format it instantly!
"""
    await message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)


@app.on_message(filters.command('help') & filters.private)
async def help_command(client: Client, message: Message):
    """Handle /help command"""
    help_message = """
ℹ️ **How to use Content Formatter Bot**

**Simply send me:**
• Any text message
• URLs (I'll fetch metadata)
• Photos/Videos/Audio with captions
• Documents with descriptions

**I will reply with:**
📝 Extracted title
📄 Description
🔗 Original link
🏷️ Auto-generated tags
📅 Date and time (IST)

**Examples:**
1. Send a YouTube link → I'll extract video title and description
2. Send an article URL → I'll fetch the article metadata
3. Send a photo with caption → I'll format it with tags
4. Send plain text → I'll structure it nicely

**Note:** I don't store anything. Every message is processed and forgotten immediately.

Questions? Just send me content and see the magic! ✨
"""
    await message.reply_text(help_message, parse_mode=ParseMode.MARKDOWN)


@app.on_message(filters.command('restart') & filters.private)
async def restart_command(client: Client, message: Message):
    """Handle /restart command - just sends a fresh start message"""
    restart_message = """
🔄 **Bot Restarted**

The bot is ready to process your messages!

Send me:
• URLs to extract metadata
• Text to format
• Media with captions
• Or type /help for more info
"""
    await message.reply_text(restart_message, parse_mode=ParseMode.MARKDOWN)


def _get_media_type(message: Message) -> str:
    """
    Detect media type from message
    
    Args:
        message: Pyrogram message object
        
    Returns:
        Media type string or empty string
    """
    if message.photo:
        return 'photo'
    elif message.video:
        return 'video'
    elif message.audio:
        return 'audio'
    elif message.voice:
        return 'voice'
    elif message.document:
        return 'document'
    elif message.animation:
        return 'animation'
    elif message.sticker:
        return 'sticker'
    
    return ''


def main():
    """Main entry point"""
    logger.info("Starting Content Formatter Bot...")
    logger.info(f"Timezone: {config.TIMEZONE}")
    logger.info(f"Metadata timeout: {config.METADATA_TIMEOUT}s")
    logger.info(f"Max tags: {config.MAX_TAGS}")
    
    # Run the bot
    app.run()


if __name__ == "__main__":
    main()
