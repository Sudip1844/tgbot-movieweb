# IntegratedServer/run_bot.py
# Run Telegram Bot separately

import asyncio
import logging
from bot.bot_main import setup_bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info("🤖 Starting Telegram Bot...")
    asyncio.run(setup_bot())