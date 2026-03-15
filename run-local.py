#!/usr/bin/env python3
"""
Gigabot Local Runner
Starts both FastAPI server and Telegram bot locally
"""

import asyncio
import threading
import logging
import os
import signal
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from main import app
import uvicorn
from tgbot.bot import run_bot

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

async def run_fastapi():
    try:
        logger.info("🚀 Starting FastAPI server on http://localhost:8000")
        config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()
    except Exception as e:
        logger.error(f"❌ FastAPI error: {e}")
        raise

def run_telegram_bot():
    try:
        logger.info("🤖 Starting Telegram bot...")
        run_bot()
    except Exception as e:
        logger.error(f"❌ Telegram bot error: {e}")

async def main():
    logger.info("🎯 Starting Gigabot Local System")
    logger.info("📱 WhatsApp webhook: http://localhost:8000/whatsapp/webhook")
    logger.info("🤖 Telegram bot: Check your bot in Telegram")

    # Start FastAPI in background
    fastapi_task = asyncio.create_task(run_fastapi())

    # Start Telegram bot in thread
    bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    bot_thread.start()

    try:
        await fastapi_task
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down...")

if __name__ == "__main__":
    print("🎯 GIGABOT LOCAL STARTER")
    print("========================")
    print("🚀 Starting FastAPI server...")
    print("🤖 Starting Telegram bot...")
    print("📱 Test webhook: http://localhost:8000/whatsapp/webhook")
    print("⏹️  Press Ctrl+C to stop")
    print("========================\n")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 System stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("Press Enter to exit...")