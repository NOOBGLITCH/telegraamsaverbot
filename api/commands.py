"""Command handlers"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from storage import save_item, get_user_settings, update_user_settings
from processor import process_url, process_text
from backup import create_export, create_backup
from .telegram import send_message, send_document
from datetime import datetime
import re

def process_command(update):
    """Process bot commands"""
    command = update.text.split()[0].lower()
    
    if command == "/start":
        handle_start(update)
    elif command == "/help":
        handle_help(update)
    elif command == "/save":
        handle_save(update)
    elif command == "/export":
        handle_export(update)
    elif command == "/backup":
        handle_backup(update)

def handle_start(update):
    """Handle /start command"""
    text = (
        f"🧠 **Welcome to MindVault, {update.first_name}!**\n\n"
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
    send_message(update.chat_id, text)

def handle_help(update):
    """Handle /help command"""
    text = (
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
    send_message(update.chat_id, text)

def handle_save(update):
    """Handle /save command"""
    parts = update.text.split(maxsplit=1)
    if len(parts) < 2:
        send_message(update.chat_id, "Usage: /save <URL or text>")
        return
    
    content = parts[1]
    save_content(update, content)

def handle_export(update):
    """Handle /export command"""
    send_message(update.chat_id, "📦 Creating export...")
    
    zip_path = create_export(str(update.from_id))
    
    if not zip_path:
        send_message(update.chat_id, "❌ No items to export")
        return
    
    send_document(update.chat_id, zip_path, "📦 Your MindVault export")
    
    # Cleanup
    import os
    os.remove(zip_path)

def handle_backup(update):
    """Handle /backup command"""
    args = update.text.split()[1:] if len(update.text.split()) > 1 else []
    
    if not args:
        text = (
            "**Backup Commands:**\n"
            "/backup now - Create backup now\n"
            "/backup on - Enable daily backups\n"
            "/backup off - Disable daily backups\n"
            "/backup status - Check status"
        )
        send_message(update.chat_id, text)
        return
    
    cmd = args[0].lower()
    
    if cmd == "now":
        send_message(update.chat_id, "💾 Creating backup...")
        zip_path = create_backup(str(update.from_id))
        if zip_path:
            send_document(update.chat_id, zip_path, "💾 Your MindVault backup")
            import os
            os.remove(zip_path)
        else:
            send_message(update.chat_id, "❌ No items to backup")
    
    elif cmd == "on":
        settings = get_user_settings(str(update.from_id))
        settings['daily_backup_enabled'] = True
        update_user_settings(str(update.from_id), settings)
        send_message(update.chat_id, "✅ Daily backups enabled!")
    
    elif cmd == "off":
        settings = get_user_settings(str(update.from_id))
        settings['daily_backup_enabled'] = False
        update_user_settings(str(update.from_id), settings)
        send_message(update.chat_id, "❌ Daily backups disabled")
    
    elif cmd == "status":
        settings = get_user_settings(str(update.from_id))
        enabled = settings.get('daily_backup_enabled', True)
        last = settings.get('last_backup', 'Never')
        status_text = "✅ ON" if enabled else "❌ OFF"
        send_message(
            update.chat_id,
            f"**Backup Status**\n\nDaily backups: {status_text}\nLast backup: {last}"
        )

def save_content(update, content):
    """Save content helper"""
    is_url = bool(re.match(r'^https?://', content.strip()))
    
    if is_url:
        data = process_url(content)
    else:
        data = process_text(content)
    
    item = {
        'user_id': str(update.from_id),
        'chat_id': str(update.chat_id),
        'message_id': str(update.message_id),
        'deeplink': f"tg://user?id={update.from_id}",
        'title': data['title'],
        'description': data['description'],
        'filename': data['filename'],
        'tags': data['tags'],
        'url': data.get('url', ''),
        'content': content,
        'timestamp': datetime.now().isoformat()
    }
    
    success = save_item(str(update.from_id), item)
    
    if success:
        tags_str = ' '.join(data['tags'])
        text = (
            f"📌 **Saved Successfully**\n\n"
            f"📄 **Title:** {data['title']}\n"
            f"🗂 **Filename:** `{data['filename']}`\n"
            f"🏷 **Tags:** {tags_str}\n"
            f"🔗 **Source:** {data.get('url', 'Direct message')}"
        )
        send_message(update.chat_id, text)
    else:
        send_message(update.chat_id, "❌ Error saving. Please try again.")
