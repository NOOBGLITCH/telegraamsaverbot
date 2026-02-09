# MindVault Telegram Bot

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FNOOBGLITCH%2Ftelegraamsaverbot&env=BOT_TOKEN,API_ID,API_HASH&envDescription=Required%20Telegram%20credentials&envLink=https%3A%2F%2Fgithub.com%2FNOOBGLITCH%2Ftelegraamsaverbot%23setup&project-name=mindvault-bot&repository-name=mindvault-bot)

Personal knowledge vault bot built with Pyrogram. Save URLs, notes, and messages with automatic tagging and export.

## ✨ Features

- 📌 Save URLs with automatic metadata extraction
- 📝 Save text notes and forwarded messages  
- 🏷️ Automatic tagging (domain + keyword based)
- 📦 Export as organized Markdown ZIP
- 💾 Daily automatic backups
- 🚀 Serverless deployment on Vercel

## 🚀 Quick Deploy

### One-Click Deploy

Click the button above to deploy to Vercel. You'll need:

1. **BOT_TOKEN** - Get from [@BotFather](https://t.me/botfather)
2. **API_ID** - Get from [my.telegram.org](https://my.telegram.org)
3. **API_HASH** - Get from [my.telegram.org](https://my.telegram.org)

### After Deployment

1. Visit `https://your-app.vercel.app/api/setWebhook` to configure the webhook
2. Start chatting with your bot!

## 📋 Setup Instructions

### Get Telegram Credentials

#### 1. Bot Token
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow instructions
3. Copy your bot token

#### 2. API Credentials
1. Go to [my.telegram.org](https://my.telegram.org)
2. Log in with your phone number
3. Navigate to "API development tools"
4. Create a new application
5. Copy your `API_ID` and `API_HASH`

### Environment Variables

```env
BOT_TOKEN=your_bot_token_from_botfather
API_ID=your_api_id_from_my_telegram_org
API_HASH=your_api_hash_from_my_telegram_org
TZ=Asia/Kolkata
```

## 💬 Commands

- `/start` - Start the bot
- `/help` - Show help message
- `/save <content>` - Save URL or text
- `/export` - Export all data as Markdown ZIP
- `/backup now` - Create manual backup
- `/backup on/off` - Toggle daily backups
- `/backup status` - Check backup status

## 📖 Usage

Just send any content to the bot:

- **URLs**: `https://example.com/article`
- **Notes**: `Remember to review the PR`
- **Forward** any message

The bot will automatically:
- Extract metadata from URLs
- Generate smart filenames
- Apply relevant tags
- Save everything for export

## 🏗️ Architecture

```
Telegram → Webhook → Vercel Serverless Function → Process → JSON Storage
```

**Serverless Functions:**
- `/api/webhook` - Receives Telegram updates
- `/api/setWebhook` - Configures webhook URL
- `/api/cron/backup` - Daily backup cron job
- `/` - Health check

## 📁 Project Structure

```
mindvault/
├── api/                    # Vercel serverless functions
│   ├── webhook.py          # Main webhook handler
│   ├── setWebhook.py       # Webhook configuration
│   ├── index.py            # Health check
│   └── cron/
│       └── backup.py       # Daily backup cron
├── main.py                 # Core bot logic
├── config.py               # Configuration
├── handlers.py             # Command handlers
├── processor.py            # Content processing
├── storage.py              # JSON storage
├── backup.py               # Export & backup
├── data/                   # Data storage
│   ├── items/              # Saved items
│   ├── users/              # User settings
│   └── exports/            # Exports
└── vercel.json             # Vercel configuration
```

## 🔧 Local Development

```bash
# Clone repository
git clone https://github.com/NOOBGLITCH/telegraamsaverbot
cd telegraamsaverbot

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your credentials

# Run locally
python main.py
```

## 🌐 How It Works (Serverless)

1. **Webhook Mode**: Bot receives updates via HTTPS webhook (no polling)
2. **Stateless**: Each request is independent, no persistent connections
3. **In-Memory Sessions**: Pyrogram sessions created per request
4. **JSON Storage**: Data stored in JSON files (serverless-compatible)
5. **Cron Jobs**: Daily backups via Vercel Cron

**Benefits:**
- ✅ Zero server costs (Vercel free tier)
- ✅ Auto-scaling
- ✅ No server management
- ✅ Global CDN
- ✅ HTTPS by default

## 📝 License

MIT

## 🤝 Contributing

Pull requests welcome!

## ⭐ Support

If you find this useful, give it a star!