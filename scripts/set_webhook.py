"""
Script to set webhook URL for Telegram bot
Run this after deploying to Vercel
"""

import os
import sys
import json
import urllib.request
import urllib.parse

def set_webhook(bot_token: str, webhook_url: str):
    """
    Set webhook URL for Telegram bot
    
    Args:
        bot_token: Telegram bot token
        webhook_url: Full webhook URL (e.g., https://your-app.vercel.app/api/webhook)
    """
    api_url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
    data = json.dumps({"url": webhook_url}).encode('utf-8')
    req = urllib.request.Request(api_url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            
        if result.get("ok"):
            print("✅ Webhook set successfully!")
            print(f"📍 Webhook URL: {webhook_url}")
            return True
        else:
            print("❌ Failed to set webhook")
            print(f"Error: {result.get('description', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def get_webhook_info(bot_token: str):
    """Get current webhook info"""
    api_url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
    
    try:
        with urllib.request.urlopen(api_url, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        if result.get("ok"):
            info = result.get("result", {})
            print("\n📊 Current Webhook Info:")
            print(f"   URL: {info.get('url', 'Not set')}")
            print(f"   Pending updates: {info.get('pending_update_count', 0)}")
            if info.get('last_error_message'):
                print(f"   Last error: {info.get('last_error_message')}")
        else:
            print("❌ Failed to get webhook info")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main function"""
    print("🤖 Telegram Webhook Setup\n")
    
    # Get bot token
    bot_token = os.environ.get("BOT_TOKEN")
    if not bot_token:
        bot_token = input("Enter your BOT_TOKEN: ").strip()
    
    if not bot_token:
        print("❌ BOT_TOKEN is required")
        sys.exit(1)
    
    # Get webhook URL
    default_url = "https://mindvault-copy.vercel.app/api/webhook"
    webhook_url = input(f"Enter your webhook URL [{default_url}]: ").strip() or default_url
    
    # Set webhook
    print("\n🔧 Setting webhook...")
    success = set_webhook(bot_token, webhook_url)
    
    if success:
        # Get webhook info
        get_webhook_info(bot_token)
        print("\n✅ Setup complete! Your bot is now running in webhook mode.")
        print("💡 Test it by sending a message to your bot on Telegram.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
