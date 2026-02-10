#!/bin/bash

# Telegram Content Formatter Bot - Setup Script
# This script helps you set up the bot quickly

set -e

echo "🚀 Telegram Content Formatter Bot - Setup"
echo "=========================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Found Python $python_version"
echo ""

# Create virtual environment
echo "🔧 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "ℹ️  Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your Telegram credentials:"
    echo "   - API_ID (from my.telegram.org)"
    echo "   - API_HASH (from my.telegram.org)"
    echo "   - BOT_TOKEN (from @BotFather)"
    echo ""
else
    echo "ℹ️  .env file already exists"
    echo ""
fi

# Create sessions directory
if [ ! -d "sessions" ]; then
    mkdir -p sessions
    echo "✅ Sessions directory created"
fi

echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python bot.py"
echo ""
echo "Or use Docker:"
echo "1. Edit .env file with your credentials"
echo "2. Run: docker-compose up -d"
echo ""
