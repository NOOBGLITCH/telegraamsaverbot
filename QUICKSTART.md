# Quick Start Guide

## Get Bot Running in 3 Steps

### Step 1: Get Credentials

1. **API ID & Hash**: Visit [my.telegram.org](https://my.telegram.org)
   - Login → API Development Tools → Create Application
   - Copy `api_id` and `api_hash`

2. **Bot Token**: Message [@BotFather](https://t.me/botfather)
   - Send `/newbot`
   - Follow instructions
   - Copy bot token

### Step 2: Configure

```bash
cp .env.example .env
nano .env  # or any editor
```

Add your credentials:
```env
API_ID=964098
API_HASH=3a40779521bc99b4c9753572ddd17ee7
BOT_TOKEN=8588040482:AAGfY_lph77iFnWPH1lJMKOiDKX8tZiEIos
```

### Step 3: Run

**Option A: Local**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python bot.py
```

**Option B: Docker**
```bash
docker-compose up -d
```

## Test Your Bot

1. Open Telegram
2. Search for your bot
3. Send `/start`
4. Try sending a URL or text

Done! 🎉
