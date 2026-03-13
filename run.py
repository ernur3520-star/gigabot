import asyncio
import threading
import logging
import signal
import sys
import os
from main import app
import uvicorn
from tgbot.bot import run_bot

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # Use stdout for Railway logs
    ]
)
logger = logging.getLogger(__name__)

# Global flag for graceful shutdown
shutdown_event = threading.Event()

def signal_handler(signum, frame):
    logger.info("Received shutdown signal, stopping services...")
    shutdown_event.set()

async def run_fastapi():
    try:
        logger.info("Starting FastAPI server...")
        config = uvicorn.Config(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
        server = uvicorn.Server(config)
        await server.serve()
    except Exception as e:
        logger.error(f"FastAPI error: {e}")
        raise

def run_telegram_bot():
    try:
        logger.info("Starting Telegram bot...")
        run_bot()
    except Exception as e:
        logger.error(f"Telegram bot error: {e}")
        # Don't re-raise to keep FastAPI running

async def main():
    logger.info("Starting Gigabot system...")

    # Setup signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Run FastAPI in background
    fastapi_task = asyncio.create_task(run_fastapi())

    # Run Telegram bot in thread (since it's blocking)
    bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    bot_thread.start()

    try:
        # Wait for FastAPI or shutdown signal
        while not shutdown_event.is_set():
            await asyncio.sleep(1)
            if fastapi_task.done():
                break
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Main loop error: {e}")
    finally:
        logger.info("Shutdown complete")

if __name__ == "__main__":
    asyncio.run(main())