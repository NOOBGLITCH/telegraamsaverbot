"""JSON-based storage module"""
import json
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from config import DATA_DIR

logger = logging.getLogger(__name__)

# File locks for concurrent access
_locks = {}

def get_lock(path: str):
    """Get lock for file path"""
    if path not in _locks:
        _locks[path] = asyncio.Lock()
    return _locks[path]

async def save_item(user_id: str, item: dict) -> bool:
    """Save item for user"""
    file_path = Path(DATA_DIR) / "items" / f"{user_id}.json"
    lock = get_lock(str(file_path))
    
    async with lock:
        try:
            # Load existing
            items = []
            if file_path.exists():
                with open(file_path, 'r') as f:
                    items = json.load(f)
            
            # Add new item
            item['id'] = f"{user_id}_{datetime.now().timestamp()}"
            items.append(item)
            
            # Save
            with open(file_path, 'w') as f:
                json.dump(items, f, indent=2)
            
            return True
        except Exception as e:
            logger.error(f"Save error: {e}")
            return False

async def get_user_items(user_id: str) -> list:
    """Get all items for user"""
    file_path = Path(DATA_DIR) / "items" / f"{user_id}.json"
    
    if not file_path.exists():
        return []
    
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except:
        return []

async def get_user_settings(user_id: str) -> dict:
    """Get user settings"""
    file_path = Path(DATA_DIR) / "users" / f"{user_id}.json"
    
    if not file_path.exists():
        return {
            'user_id': user_id,
            'daily_backup_enabled': True,
            'created_at': datetime.now().isoformat()
        }
    
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except:
        return {'user_id': user_id, 'daily_backup_enabled': True}

async def update_user_settings(user_id: str, settings: dict) -> bool:
    """Update user settings"""
    file_path = Path(DATA_DIR) / "users" / f"{user_id}.json"
    lock = get_lock(str(file_path))
    
    async with lock:
        try:
            settings['updated_at'] = datetime.now().isoformat()
            with open(file_path, 'w') as f:
                json.dump(settings, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Settings update error: {e}")
            return False

async def get_all_users() -> list:
    """Get all user IDs"""
    items_dir = Path(DATA_DIR) / "items"
    return [f.stem for f in items_dir.glob("*.json")]
