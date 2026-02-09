"""
MindVault Telegram Bot - Main Application
Pyrogram-based serverless bot for personal knowledge management
"""

import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from fastapi import FastAPI
from config import API_ID, API_HASH, BOT_TOKEN
from handlers import (
    handle_start, handle_help, handle_save, 
    handle_export, handle_backup, handle_message
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI app for health checks and cron
app = FastAPI(title="MindVault Bot")

# Pyrogram bot client
bot = Client(
    "mindvault",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workdir="./sessions"
)

# Command handlers
@bot.on_message(filters.command("start") & filters.private)
async def start(client: Client, message: Message):
    await handle_start(client, message)

@bot.on_message(filters.command("help") & filters.private)
async def help_cmd(client: Client, message: Message):
    await handle_help(client, message)

@bot.on_message(filters.command("save") & filters.private)
async def save(client: Client, message: Message):
    await handle_save(client, message)

@bot.on_message(filters.command("export") & filters.private)
async def export(client: Client, message: Message):
    await handle_export(client, message)

@bot.on_message(filters.command("backup") & filters.private)
async def backup(client: Client, message: Message):
    await handle_backup(client, message)

@bot.on_message(filters.text & ~filters.command & filters.private)
async def message(client: Client, message: Message):
    await handle_message(client, message)

# FastAPI routes
@app.on_event("startup")
async def startup():
    logger.info("Starting MindVault Bot...")
    await bot.start()
    logger.info("Bot started successfully!")

@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutting down bot...")
    await bot.stop()

@app.get("/")
async def health():
    return {"status": "running", "bot": "MindVault"}

@app.get("/api/cron/backup")
async def cron_backup():
    """Daily backup cron job"""
    try:
        from backup import run_daily_backup
        await run_daily_backup(bot)
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)