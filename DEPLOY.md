# Deploy MindVault Bot

## Vercel Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd /home/edith/Documents/mindvault
vercel
```

## Environment Variables

Set in Vercel dashboard:

```env
BOT_TOKEN=8588040482:AAGfY_lph77iFnWPH1lJMKOiDKX8tZiEIos
API_ID=964098
API_HASH=3a40779521bc99b4c9753572ddd17ee7
DATA_DIR=./data
TZ=Asia/Kolkata
```

## Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run bot
python main.py
```

Bot will start on `http://localhost:8000`

## Cron Job

Add to `vercel.json`:

```json
{
  "crons": [{
    "path": "/api/cron/backup",
    "schedule": "0 0 * * *"
  }]
}
```

This runs daily backups at midnight IST.

## Ready!

Your bot is now deployed and ready to use.