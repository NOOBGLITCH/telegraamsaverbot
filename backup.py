"""Backup and export functionality"""
import zipfile
import logging
from pathlib import Path
from datetime import datetime
from io import BytesIO
from storage import get_user_items, get_all_users, get_user_settings, update_user_settings
from config import DATA_DIR

logger = logging.getLogger(__name__)

def generate_markdown(item: dict) -> str:
    """Generate markdown for item"""
    md = f"# {item.get('title', 'Untitled')}\n\n"
    
    if item.get('description'):
        md += f"{item['description']}\n\n"
    
    md += "---\n\n"
    md += f"**Tags:** {' '.join(item.get('tags', []))}\n\n"
    
    if item.get('url'):
        md += f"**Source:** [{item['url']}]({item['url']})\n\n"
    
    md += f"**Saved:** {item.get('timestamp', '')}\n\n"
    
    if item.get('content') and item['content'] != item.get('url'):
        md += f"## Content\n\n{item['content']}\n"
    
    return md

async def create_export(user_id: str) -> str:
    """Create export ZIP for user"""
    items = await get_user_items(user_id)
    
    if not items:
        return None
    
    # Create temp ZIP
    zip_path = f"/tmp/mindvault-export-{user_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Group by tags
        tag_items = {}
        for item in items:
            tags = item.get('tags', ['#uncategorized'])
            for tag in tags:
                tag_clean = tag.replace('#', '').replace('/', '-')
                if tag_clean not in tag_items:
                    tag_items[tag_clean] = []
                tag_items[tag_clean].append(item)
        
        # Add files
        for tag, tag_list in tag_items.items():
            for item in tag_list:
                filename = item.get('filename', 'note.md')
                path = f"{tag}/{filename}"
                md = generate_markdown(item)
                zf.writestr(path, md)
        
        # Add INDEX
        index = f"# MindVault Export\n\nGenerated: {datetime.now()}\n\nTotal items: {len(items)}\n\n"
        index += "## Tags\n\n"
        for tag in sorted(tag_items.keys()):
            index += f"- [{tag}](./{tag}/)\n"
        zf.writestr("INDEX.md", index)
    
    return zip_path

async def create_backup(user_id: str) -> str:
    """Create backup ZIP for user"""
    return await create_export(user_id)

async def run_daily_backup(bot):
    """Run daily backup for all users"""
    users = await get_all_users()
    
    for user_id in users:
        try:
            settings = await get_user_settings(user_id)
            
            if not settings.get('daily_backup_enabled', True):
                continue
            
            zip_path = await create_backup(user_id)
            
            if zip_path:
                # Send to user
                await bot.send_document(
                    chat_id=int(user_id),
                    document=zip_path,
                    caption="💾 Daily backup"
                )
                
                # Update settings
                settings['last_backup'] = datetime.now().isoformat()
                await update_user_settings(user_id, settings)
                
                # Cleanup
                import os
                os.remove(zip_path)
                
                logger.info(f"Backup sent to {user_id}")
        
        except Exception as e:
            logger.error(f"Backup failed for {user_id}: {e}")
