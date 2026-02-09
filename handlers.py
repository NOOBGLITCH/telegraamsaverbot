"""Bot command handlers"""
import logging
import re
from pyrogram import Client
from pyrogram.types import Message
from processor import process_url, process_text
from storage import save_item, get_user_items, get_user_settings, update_user_settings
from backup import create_export, create_backup
from datetime import datetime

logger = logging.getLogger(__name__)

async def handle_start(client: Client, message: Message):
    """Handle /start command"""
    user = message.from_user
    await message.reply_text(
        f"🧠 **Welcome to MindVault, {user.first_name}!**\n\n"
        "I help you save and organize:\n"
        "• URLs (articles, videos, blogs)\n"
        "• Text notes\n"
        "• Forwarded messages\n\n"
        "Just send me any content and I'll:\n"
        "✓ Extract metadata\n"
        "✓ Generate smart filenames\n"
        "✓ Apply relevant tags\n"
        "✓ Save for easy export\n\n"
        "Use /help to see all commands."
    )

async def handle_help(client: Client, message: Message):
    """Handle /help command"""
    await message.reply_text(
        "**Commands:**\n"
        "/start - Start the bot\n"
        "/help - Show this help\n"
        "/save <content> - Save URL or text\n"
        "/export - Export all data as Markdown ZIP\n"
        "/backup now - Create manual backup\n"
        "/backup on - Enable daily backups\n"
        "/backup off - Disable daily backups\n"
        "/backup status - Check backup status\n\n"
        "**Usage:**\n"
        "• Send any URL to save it\n"
        "• Send text notes directly\n"
        "• Forward messages to save them"
    )

async def handle_save(client: Client, message: Message):
    """Handle /save command"""
    text = message.text.split(maxsplit=1)
    if len(text) < 2:
        await message.reply_text("Usage: /save <URL or text>")
        return
    
    content = text[1]
    await process_and_save(client, message, content)

async def handle_message(client: Client, message: Message):
    """Handle regular messages"""
    if not message.text:
        return
    
    content = message.text
    
    # Add forward info if forwarded
    if message.forward_date:
        if message.forward_from:
            content += f"\n\nForwarded from: {message.forward_from.first_name}"
        elif message.forward_from_chat:
            content += f"\n\nForwarded from: {message.forward_from_chat.title}"
    
    await process_and_save(client, message, content)

async def process_and_save(client: Client, message: Message, content: str):
    """Process and save content"""
    user = message.from_user
    status = await message.reply_text("🔄 Processing...")
    
    try:
        # Detect if URL
        is_url = bool(re.match(r'^https?://', content.strip()))
        
        # Process content
        if is_url:
            data = await process_url(content)
        else:
            data = process_text(content)
        
        # Save to storage
        item = {
            'user_id': str(user.id),
            'chat_id': str(message.chat.id),
            'message_id': str(message.id),
            'deeplink': f"tg://user?id={user.id}",
            'title': data['title'],
            'description': data['description'],
            'filename': data['filename'],
            'tags': data['tags'],
            'url': data.get('url', ''),
            'content': content,
            'timestamp': datetime.now().isoformat()
        }
        
        success = await save_item(str(user.id), item)
        
        if success:
            await status.delete()
            tags_str = ' '.join(data['tags'])
            await message.reply_text(
                f"📌 **Saved Successfully**\n\n"
                f"📄 **Title:** {data['title']}\n"
                f"🗂 **Filename:** `{data['filename']}`\n"
                f"🏷 **Tags:** {tags_str}\n"
                f"🔗 **Source:** {data.get('url', 'Direct message')}"
            )
        else:
            await status.edit_text("❌ Error saving. Please try again.")
    
    except Exception as e:
        logger.error(f"Error: {e}")
        await status.edit_text(f"❌ Error: {str(e)}")

async def handle_export(client: Client, message: Message):
    """Handle /export command"""
    user = message.from_user
    status = await message.reply_text("📦 Creating export...")
    
    try:
        zip_path = await create_export(str(user.id))
        
        if not zip_path:
            await status.edit_text("❌ No items to export")
            return
        
        await status.delete()
        await message.reply_document(
            document=zip_path,
            caption="📦 Your MindVault export"
        )
        
        # Cleanup
        import os
        os.remove(zip_path)
    
    except Exception as e:
        logger.error(f"Export error: {e}")
        await status.edit_text(f"❌ Error: {str(e)}")

async def handle_backup(client: Client, message: Message):
    """Handle /backup command"""
    user = message.from_user
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    
    if not args:
        await message.reply_text(
            "**Backup Commands:**\n"
            "/backup now - Create backup now\n"
            "/backup on - Enable daily backups\n"
            "/backup off - Disable daily backups\n"
            "/backup status - Check status"
        )
        return
    
    cmd = args[0].lower()
    
    if cmd == "now":
        status = await message.reply_text("💾 Creating backup...")
        try:
            zip_path = await create_backup(str(user.id))
            if zip_path:
                await status.delete()
                await message.reply_document(
                    document=zip_path,
                    caption="💾 Your MindVault backup"
                )
                import os
                os.remove(zip_path)
            else:
                await status.edit_text("❌ No items to backup")
        except Exception as e:
            await status.edit_text(f"❌ Error: {str(e)}")
    
    elif cmd == "on":
        settings = await get_user_settings(str(user.id))
        settings['daily_backup_enabled'] = True
        await update_user_settings(str(user.id), settings)
        await message.reply_text("✅ Daily backups enabled!")
    
    elif cmd == "off":
        settings = await get_user_settings(str(user.id))
        settings['daily_backup_enabled'] = False
        await update_user_settings(str(user.id), settings)
        await message.reply_text("❌ Daily backups disabled")
    
    elif cmd == "status":
        settings = await get_user_settings(str(user.id))
        enabled = settings.get('daily_backup_enabled', True)
        last = settings.get('last_backup', 'Never')
        status_text = "✅ ON" if enabled else "❌ OFF"
        await message.reply_text(
            f"**Backup Status**\n\n"
            f"Daily backups: {status_text}\n"
            f"Last backup: {last}"
        )