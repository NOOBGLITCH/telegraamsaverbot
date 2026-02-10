# Deployment Guide - Serverless Telegram Bot

Complete guide to deploy your Telegram Content Formatter Bot to Vercel or Netlify.

## Prerequisites

- Telegram Bot Token (get from [@BotFather](https://t.me/botfather))
- Vercel or Netlify account
- Git repository (optional but recommended)

## Quick Deploy

### Deploy to Vercel (Recommended)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/NOOBGLITCH/telegraamsaverbot&env=BOT_TOKEN&envDescription=Telegram%20Bot%20Token%20from%20BotFather&project-name=telegram-content-bot&repository-name=telegram-content-bot)

### Deploy to Netlify

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/NOOBGLITCH/telegraamsaverbot)

---

## Manual Deployment Steps

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Deploy to Vercel

```bash
cd /path/to/your/project
vercel --prod
```

Follow the prompts:
- Set up and deploy? **Y**
- Which scope? Select your account
- Link to existing project? **N**
- Project name? Enter a name (e.g., `telegram-content-bot`)
- Directory? Press Enter (use current directory)
- Override settings? **N**

### Step 3: Set Environment Variables

In Vercel Dashboard:

1. Go to your project → Settings → Environment Variables
2. Add the following variables:

| Variable | Value | Required |
|----------|-------|----------|
| `BOT_TOKEN` | Your Telegram bot token | ✅ Yes |
| `TIMEZONE` | `Asia/Kolkata` (or your timezone) | ❌ Optional |
| `METADATA_TIMEOUT` | `5` | ❌ Optional |
| `MAX_TAGS` | `8` | ❌ Optional |

**Or via CLI:**

```bash
vercel env add BOT_TOKEN
# Paste your bot token when prompted
```

### Step 4: Register Webhook

After deployment, you'll get a URL like: `https://your-app.vercel.app`

Run the webhook setup script:

```bash
cd scripts
pip install httpx
python set_webhook.py
```

Enter:
- **BOT_TOKEN**: Your Telegram bot token
- **Webhook URL**: `https://your-app.vercel.app/api/webhook`

### Step 5: Test Your Bot

1. Open Telegram
2. Find your bot
3. Send a message or URL
4. Bot should respond with formatted content!

---

## Netlify Deployment

### Using Netlify CLI

```bash
npm install -g netlify-cli
netlify deploy --prod
```

### Configure Netlify

Create `netlify.toml`:

```toml
[build]
  command = "echo 'No build needed'"
  publish = "."

[functions]
  directory = "api"
  node_bundler = "esbuild"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200
```

**Note:** Netlify has different serverless function structure. Vercel is recommended for Python serverless functions.

---

## Troubleshooting

### Bot Not Responding

1. **Check Vercel Logs:**
   ```bash
   vercel logs
   ```

2. **Verify Webhook:**
   ```bash
   curl https://api.telegram.org/bot<YOUR_TOKEN>/getWebhookInfo
   ```

3. **Check Environment Variables:**
   - Ensure `BOT_TOKEN` is set in Vercel dashboard
   - Redeploy after adding variables

### Webhook Errors

- **Invalid token:** Check if `BOT_TOKEN` is correct
- **URL not HTTPS:** Vercel provides HTTPS by default
- **Timeout:** Increase `METADATA_TIMEOUT` if needed

### Function Timeout

Vercel free tier has 10s timeout. If metadata fetching is slow:
- Reduce `METADATA_TIMEOUT` to 3-5 seconds
- Consider upgrading Vercel plan

---

## Local Testing

### Test Locally Before Deployment

```bash
cd api
pip install -r requirements.txt
uvicorn webhook:app --reload --port 8000
```

### Test with ngrok

```bash
ngrok http 8000
```

Use the ngrok HTTPS URL to set webhook temporarily for testing.

---

## Monitoring

### View Logs

**Vercel:**
```bash
vercel logs --follow
```

**Or in Dashboard:**
- Go to your project → Deployments → Click latest → View Function Logs

### Webhook Info

Check webhook status:
```bash
curl https://api.telegram.org/bot<YOUR_TOKEN>/getWebhookInfo
```

---

## Updating Your Bot

### Push Updates

```bash
git add .
git commit -m "Update bot"
git push
```

Vercel auto-deploys on push if connected to Git.

### Manual Redeploy

```bash
vercel --prod
```

---

## Security Best Practices

1. ✅ Never commit `.env` file
2. ✅ Use environment variables for secrets
3. ✅ Keep `BOT_TOKEN` private
4. ✅ Use HTTPS only (Vercel provides this)
5. ✅ Regularly update dependencies

---

## Cost

- **Vercel Free Tier:** 
  - 100GB bandwidth/month
  - 100 hours serverless function execution
  - Sufficient for personal bots

- **Netlify Free Tier:**
  - 100GB bandwidth/month
  - 125k function requests/month

---

## Support

- 📚 [Vercel Documentation](https://vercel.com/docs)
- 📚 [Telegram Bot API](https://core.telegram.org/bots/api)
- 🐛 [Report Issues](https://github.com/NOOBGLITCH/telegraamsaverbot/issues)
