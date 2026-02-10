"""
Telegram Instant Content Formatter Bot - Serverless Webhook Handler
FastAPI-based webhook for Vercel deployment

Framework: FastAPI
Architecture: Stateless serverless functions
"""

import os
import re
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx

# Import local modules
from .config import BOT_TOKEN, validate_config
from .utils import (
    get_first_valid_url,
    fetch_metadata,
    generate_tags,
    format_response,
    get_current_ist_time
)

# Validate configuration on startup
validate_config()

# Initialize FastAPI app
app = FastAPI(title="Telegram Content Formatter Bot")

# Telegram API endpoint
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


async def send_message(chat_id: int, text: str, parse_mode: str = "HTML") -> Dict[str, Any]:
    """
    Send message to Telegram chat
    
    Args:
        chat_id: Telegram chat ID
        text: Message text
        parse_mode: Parse mode (HTML or Markdown)
        
    Returns:
        API response
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": parse_mode
            }
        )
        return response.json()


def get_media_type(message: Dict[str, Any]) -> str:
    """
    Detect media type from message
    
    Args:
        message: Telegram message object
        
    Returns:
        Media type string or empty string
    """
    media_types = ['photo', 'video', 'audio', 'voice', 'document', 'animation', 'sticker']
    for media_type in media_types:
        if media_type in message:
            return media_type
    return ''


def format_media_only_message(media_type: str, timestamp: datetime) -> str:
    """Format message for media without caption"""
    emoji_map = {
        'photo': '🖼️', 'video': '🎥', 'audio': '🎵', 'voice': '🎤',
        'document': '📄', 'animation': '🎬', 'sticker': '✨'
    }
    
    emoji = emoji_map.get(media_type.lower(), '📎')
    date = timestamp.strftime("%d %b %Y")
    time = timestamp.strftime("%I:%M %p IST")
    
    return (
        f"{emoji} <b>{media_type.capitalize()} Received</b>\n\n"
        f"ℹ️ No caption or text provided.\n\n"
        f"📅 <b>Date:</b> {date}\n"
        f"⏰ <b>Time:</b> {time}"
    )


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "bot": "Telegram Content Formatter", "mode": "webhook"}


@app.post("/api/webhook")
async def webhook(request: Request):
    """
    Main webhook handler for Telegram updates
    
    Processes incoming messages and sends formatted responses
    """
    try:
        # Parse incoming update
        update = await request.json()
        
        # Extract message (handle both new messages and edited messages)
        message = update.get("message") or update.get("edited_message")
        
        if not message:
            return JSONResponse({"ok": True})
        
        # Get chat ID and user info
        chat_id = message["chat"]["id"]
        
        # Handle commands
        text = message.get("text", "")
        
        if text.startswith("/start"):
            welcome_message = """
👋 <b>Welcome to Content Formatter Bot!</b>

I'm a stateless bot that instantly formats any content you send me.

<b>What I do:</b>
✅ Extract metadata from URLs
✅ Generate automatic tags
✅ Format content beautifully
✅ Add IST timestamps

<b>What I support:</b>
📝 Text messages
🔗 URLs and links
🖼️ Photos with captions
🎥 Videos with captions
🎵 Audio with captions
📄 Documents with captions

<b>Privacy:</b>
🔒 No data storage
🔒 No user tracking
🔒 Instant processing and forgetting

Just send me anything, and I'll format it instantly!
"""
            await send_message(chat_id, welcome_message)
            return JSONResponse({"ok": True})
        
        if text.startswith("/help"):
            help_message = """
ℹ️ <b>How to use Content Formatter Bot</b>

<b>Simply send me:</b>
• Any text message
• URLs (I'll fetch metadata)
• Photos/Videos/Audio with captions
• Documents with descriptions

<b>I will reply with:</b>
📝 Extracted title
📄 Description
🔗 Original link
🏷️ Auto-generated tags
📅 Date and time (IST)

<b>Examples:</b>
1. Send a YouTube link → I'll extract video title and description
2. Send an article URL → I'll fetch the article metadata
3. Send a photo with caption → I'll format it with tags
4. Send plain text → I'll structure it nicely

<b>Note:</b> I don't store anything. Every message is processed and forgotten immediately.

Questions? Just send me content and see the magic! ✨
"""
            await send_message(chat_id, help_message)
            return JSONResponse({"ok": True})
        
        # Get current timestamp
        timestamp = get_current_ist_time()
        
        # Extract text content (from message or caption)
        text_content = message.get("text") or message.get("caption") or ''
        
        # Detect media type
        media_type = get_media_type(message)
        
        # If no text and no media, skip
        if not text_content and not media_type:
            return JSONResponse({"ok": True})
        
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
            except Exception:
                # Continue with fallback values
                pass
        
        # If no URL and no meaningful text, handle media-only case
        if not url and not text_content.strip():
            if media_type:
                response = format_media_only_message(media_type, timestamp)
                await send_message(chat_id, response)
            return JSONResponse({"ok": True})
        
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
        await send_message(chat_id, response)
        
        return JSONResponse({"ok": True})
        
    except Exception as e:
        # Log error but return ok to Telegram
        print(f"Error processing webhook: {e}")
        return JSONResponse({"ok": True})


# Vercel serverless function handler
handler = app
