# Telegram Content Formatter Bot 🤖

A stateless, serverless Telegram bot that instantly formats content, extracts metadata from URLs, and generates smart tags.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/NOOBGLITCH/telegraamsaverbot&env=BOT_TOKEN&envDescription=Telegram%20Bot%20Token%20from%20BotFather&project-name=telegram-content-bot&repository-name=telegram-content-bot)
[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/NOOBGLITCH/telegraamsaverbot)

## ✨ Features

- 🔗 **URL Metadata Extraction** - Automatically fetches titles and descriptions from links
- 🏷️ **Smart Tag Generation** - AI-powered tag generation based on content
- 📝 **Content Formatting** - Beautiful HTML formatting for all messages
- 🕐 **IST Timestamps** - Automatic timestamp in Indian Standard Time
- 🔒 **Privacy First** - Stateless design, no data storage
- ⚡ **Serverless** - Deploy to Vercel/Netlify in one click
- 🎯 **Media Support** - Handles photos, videos, documents with captions

## 🚀 Quick Start

### 1. Get a Bot Token

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow instructions
3. Copy your bot token

### 2. Deploy (Choose One)

#### Option A: Deploy to Vercel (Recommended)

Click the button above or:

```bash
npm install -g vercel
git clone https://github.com/NOOBGLITCH/telegraamsaverbot.git
cd telegraamsaverbot
vercel --prod
```

#### Option B: Deploy to Netlify

Click the button above or use Netlify CLI.

### 3. Set Environment Variables

In your deployment platform dashboard, add:

```
BOT_TOKEN=your_bot_token_here
TIMEZONE=Asia/Kolkata
```

### 4. Register Webhook

```bash
cd scripts
pip install httpx
python set_webhook.py
```

Enter your webhook URL: `https://your-app.vercel.app/api/webhook`

### 5. Start Using!

Send any message or URL to your bot on Telegram! 🎉

## 📖 Documentation

- [Deployment Guide](DEPLOYMENT.md) - Detailed deployment instructions
- [Quick Start](QUICKSTART.md) - Get started in 5 minutes

## 🛠️ Tech Stack

- **Framework:** FastAPI (async webhook handler)
- **Deployment:** Vercel Serverless Functions
- **HTTP Client:** httpx (async)
- **HTML Parsing:** BeautifulSoup4 + lxml
- **Architecture:** Stateless, no database required

## 📋 What It Does

Send the bot:
- **URLs** → Extracts metadata and formats beautifully
- **Text** → Structures with tags and timestamps
- **Media + Caption** → Formats with smart tags
- **Plain text** → Organizes with auto-generated tags

Example response:
```
📌 Content Saved

📝 Title:
How to Build Serverless Telegram Bots

📄 Description:
Complete guide to building and deploying serverless Telegram bots...

🔗 Link:
https://example.com/article

🏷️ Tags:
#Tutorial #Telegram #Serverless #Python

📅 Date: 10 Feb 2026
⏰ Time: 11:35 AM IST
```

## 🔧 Local Development

```bash
# Clone repository
git clone https://github.com/NOOBGLITCH/telegraamsaverbot.git
cd telegraamsaverbot

# Install dependencies
cd api
pip install -r requirements.txt

# Set environment variables
export BOT_TOKEN=your_token_here

# Run locally
uvicorn webhook:app --reload --port 8000

# Test with ngrok
ngrok http 8000
```

## 📁 Project Structure

```
telegraamsaverbot/
├── api/
│   ├── webhook.py          # Main FastAPI webhook handler
│   ├── config.py           # Configuration
│   ├── requirements.txt    # Dependencies
│   └── utils/              # Utility modules
│       ├── metadata_fetcher.py
│       ├── tag_generator.py
│       ├── url_extractor.py
│       └── formatter.py
├── scripts/
│   └── set_webhook.py      # Webhook registration script
├── vercel.json             # Vercel configuration
├── DEPLOYMENT.md           # Deployment guide
└── README.md               # This file
```

## 🌟 Key Features Explained

### Metadata Extraction
- Supports Open Graph, Twitter Cards, and standard meta tags
- Handles redirects automatically
- Timeout protection (5s default)
- Security: Blocks private IP ranges

### Tag Generation
- Domain-based tags (YouTube, GitHub, etc.)
- TF-IDF-like keyword scoring
- Priority keywords for tech topics
- Category detection
- Media type tags

### Formatting
- HTML formatting for Telegram
- Emoji indicators
- Clean, readable layout
- IST timezone support

## 🔒 Privacy & Security

- ✅ **No data storage** - Processes and forgets immediately
- ✅ **No user tracking** - Stateless architecture
- ✅ **No database** - Zero persistence
- ✅ **Secure** - Blocks private IP ranges
- ✅ **HTTPS only** - Vercel provides SSL

## 📊 Performance

- ⚡ Response time: < 3 seconds
- 🚀 Serverless auto-scaling
- 💰 Free tier friendly
- 🌍 Global CDN (Vercel)

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Deployed on [Vercel](https://vercel.com/)
- Inspired by serverless architecture patterns

## 📞 Support

- 🐛 [Report Issues](https://github.com/NOOBGLITCH/telegraamsaverbot/issues)
- 💬 [Discussions](https://github.com/NOOBGLITCH/telegraamsaverbot/discussions)
- 📧 Contact: [Your Email]

## 🎯 Roadmap

- [ ] Multi-language support
- [ ] Custom tag templates
- [ ] Webhook security token
- [ ] Rate limiting
- [ ] Analytics dashboard

---

**Made with ❤️ for the Telegram community**

⭐ Star this repo if you find it useful!
