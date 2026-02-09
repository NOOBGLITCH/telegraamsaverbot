"""Telegram Update parser"""

class Update:
    """Parse Telegram update data"""
    
    def __init__(self, update_data):
        self.raw = update_data
        self.message = update_data.get("message", {})
        
        # User info
        self.from_user = self.message.get("from", {})
        self.from_id = self.from_user.get("id")
        self.user_name = self.from_user.get("username", "")
        self.first_name = self.from_user.get("first_name", "")
        
        # Chat info
        self.chat = self.message.get("chat", {})
        self.chat_id = self.chat.get("id")
        self.is_group = self.chat.get("type") in ["group", "supergroup"]
        self.group_name = self.chat.get("title", "")
        
        # Message content
        self.message_id = self.message.get("message_id")
        self.text = self.message.get("text", "")
        self.caption = self.message.get("caption", "")
        
        # Message type
        self.type = self._detect_type()
        
        # Photo
        if "photo" in self.message:
            photos = self.message["photo"]
            self.file_id = photos[-1]["file_id"] if photos else None
            self.photo_caption = self.caption
        else:
            self.file_id = None
            self.photo_caption = ""
        
        # Forward info
        self.forward_date = self.message.get("forward_date")
        self.forward_from = self.message.get("forward_from", {})
        self.forward_from_chat = self.message.get("forward_from_chat", {})
    
    def _detect_type(self):
        """Detect message type"""
        if self.text.startswith("/"):
            return "command"
        elif "photo" in self.message:
            return "photo"
        elif self.text:
            return "text"
        else:
            return "unknown"

def send_message(chat_id, text, reply_to_message_id=None):
    """Send message via Telegram API"""
    import requests
    from .config import BOT_TOKEN
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    
    if reply_to_message_id:
        data["reply_to_message_id"] = reply_to_message_id
    
    try:
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

def send_document(chat_id, document_path, caption=""):
    """Send document via Telegram API"""
    import requests
    from .config import BOT_TOKEN
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    
    try:
        with open(document_path, 'rb') as doc:
            files = {'document': doc}
            data = {
                'chat_id': chat_id,
                'caption': caption
            }
            response = requests.post(url, files=files, data=data)
            return response.json()
    except Exception as e:
        print(f"Error sending document: {e}")
        return None
