# IntegratedServer/main.py
# Single entry point: runs Flask server + Telegram bot together
# Usage: python main.py

import os
import sys
import logging
import threading
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv(Path(__file__).parent / '.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Reduce noisy loggers
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('telegram.ext._application').setLevel(logging.WARNING)


def run_flask():
    """Run Flask server (API + Frontend) on port 5000"""
    from server.app import create_app
    app = create_app()

    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))

    logger.info(f"🌐 Flask server on http://localhost:{port}")
    logger.info(f"   📄 Home: http://localhost:{port}")
    logger.info(f"   👑 Owner: http://localhost:{port}/sudip")
    logger.info(f"   🔧 Admin: http://localhost:{port}/admin")
    logger.info(f"   📡 API: http://localhost:{port}/api/health")

    app.run(host=host, port=port, debug=False, use_reloader=False)


def run_bot():
    """Run Telegram bot in a separate thread"""
    from bot.bot_main import run_bot_in_thread
    logger.info("🤖 Starting Telegram bot in background...")
    try:
        run_bot_in_thread()
    except Exception as e:
        logger.error(f"❌ Bot error: {e}")


def main():
    print()
    print("=" * 50)
    print("  🎬 MovieZone Integrated Server")
    print("  📡 Flask API + Telegram Bot")
    print("=" * 50)
    print()

    # Start bot in a background thread
    bot_thread = threading.Thread(target=run_bot, daemon=True, name="TelegramBot")
    bot_thread.start()

    # Run Flask in main thread (blocks)
    try:
        run_flask()
    except KeyboardInterrupt:
        logger.info("🛑 Server shutting down...")
    except Exception as e:
        logger.error(f"❌ Flask error: {e}")


if __name__ == '__main__':
    main()
