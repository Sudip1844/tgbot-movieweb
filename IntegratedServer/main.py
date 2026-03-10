# IntegratedServer/main.py
# Main entry point for the integrated application

import logging
import threading
import asyncio
from server.app import create_app
from config import Config, BOT_TOKEN, OWNER_ID

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def run_bot():
    """Run Telegram Bot in async mode"""
    try:
        if not BOT_TOKEN or not OWNER_ID:
            logger.warning("⚠️ Bot not configured (missing BOT_TOKEN or OWNER_ID)")
            return
        
        logger.info("🤖 Starting Telegram Bot...")
        
        # Bot setup will be done in bot module
        from bot.bot_main import setup_bot
        await setup_bot()
        
    except Exception as e:
        logger.error(f"❌ Bot error: {e}")

def run_bot_in_thread():
    """Run bot in separate thread"""
    try:
        logger.info("🧵 Starting bot in background thread...")
        from bot.bot_main import setup_bot
        asyncio.run(setup_bot())
    except Exception as e:
        logger.error(f"❌ Thread error: {e}")

def main():
    """Main application entry"""
    
    # Banner
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║         MovieZone - Integrated Server                     ║
    ║     Telegram Bot + Web Server (Unified Python)            ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    logger.info("🚀 Starting MovieZone Integrated Server...")
    
    # Create Flask app
    app = create_app()
    
    # Start bot in background thread (optional)
    if BOT_TOKEN and OWNER_ID:
        logger.info("✅ Bot credentials configured")
        logger.info("💡 Run bot separately: python run_bot.py")
        # bot_thread = threading.Thread(target=run_bot_in_thread, daemon=True)
        # bot_thread.start()
    else:
        logger.warning("⚠️ Bot will not start (missing credentials)")
    
    # Start Flask server
    try:
        host = Config.HOST
        port = Config.PORT
        debug = Config.DEBUG
        
        logger.info(f"🌐 Flask Server: http://{host}:{port}")
        logger.info(f"📊 Access API at: http://localhost:{port}/api")
        logger.info(f"🎬 Frontend will be at: http://localhost:{port}")
        logger.info("")
        
        app.run(
            host=host,
            port=port,
            debug=debug,
            use_reloader=debug,
            threaded=True
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
