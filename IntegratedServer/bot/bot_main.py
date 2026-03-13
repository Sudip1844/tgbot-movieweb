# IntegratedServer/bot/bot_main.py
# Main bot entry point - adapted from Tgbot/main.py
# Runs the Telegram bot with all handlers

import logging
import asyncio
import os
import sys

# Add parent and current dir to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from telegram import Update, ChatMember, ChatMemberUpdated
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ChatMemberHandler, ContextTypes

from bot.config import BOT_TOKEN, BOT_USERNAME, OWNER_ID, CONVERSATION_TIMEOUT
import bot.database as db

logger = logging.getLogger(__name__)


# --- Auto-Delete Job Functions ---
async def delete_message_job(context):
    """Deletes a message after a specified time."""
    try:
        await context.bot.delete_message(chat_id=context.job.data['chat_id'],
                                         message_id=context.job.data['message_id'])
    except Exception as e:
        logger.error(f"Failed to delete message: {e}")


def schedule_message_deletion(context, chat_id: int, message_id: int, delay_seconds: int = 86400):
    """Schedules a message to be deleted after a delay."""
    context.job_queue.run_once(
        delete_message_job,
        when=delay_seconds,
        data={'chat_id': chat_id, 'message_id': message_id}
    )


# --- Channel Member Handler ---
def extract_status_change(chat_member_update: ChatMemberUpdated):
    """Extract status change from ChatMemberUpdated."""
    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = old_status in [ChatMember.MEMBER, ChatMember.OWNER, ChatMember.ADMINISTRATOR] or (
            old_status == ChatMember.RESTRICTED and old_is_member is True)
    is_member = new_status in [ChatMember.MEMBER, ChatMember.OWNER, ChatMember.ADMINISTRATOR] or (
            new_status == ChatMember.RESTRICTED and new_is_member is True)

    return was_member, is_member


async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Greets new users in chats."""
    result = extract_status_change(update.chat_member)
    if result is None:
        return
    was_member, is_member = result
    if not was_member and is_member:
        new_user = update.chat_member.new_chat_member.user
        await update.effective_chat.send_message(
            f"Welcome {new_user.mention_html()} to our channel & bot! 🎬\n\n"
            f"Use @{BOT_USERNAME} to search and download movies!",
            parse_mode='HTML'
        )


# --- Global Cancel Handler ---
async def global_cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /cancel command globally."""
    user_role = db.get_user_role(update.effective_user.id)
    from bot.utils import get_main_keyboard
    keyboard = get_main_keyboard(user_role)
    await update.message.reply_text("❌ Operation cancelled.", reply_markup=keyboard)


# --- Error Handler ---
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log errors."""
    logger.error(f"Exception while handling an update: {context.error}")


def build_application():
    """Build the bot Application with all handlers registered"""
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN not configured!")
        return None

    logger.info(f"🤖 Building Telegram Bot: @{BOT_USERNAME}")

    # Initialize database
    db.initialize_database()

    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Import handlers from copied Tgbot code
    from bot.handlers.start_handler import start_handlers
    from bot.handlers.movie_handlers import (
        request_movie_conv, remove_movie_conv, show_stats_conv,
        search_movies, handle_search_query, browse_categories
    )
    from bot.handlers.conversation_handlers import add_movie_conv_handler
    from bot.handlers.callback_handler import callback_query_handler
    from bot.handlers.owner_handlers import owner_handlers

    # Register conversation handlers first (they take priority)
    application.add_handler(add_movie_conv_handler)
    application.add_handler(request_movie_conv)
    application.add_handler(remove_movie_conv)
    application.add_handler(show_stats_conv)

    # Register owner handlers
    for handler in owner_handlers:
        application.add_handler(handler)

    # Register start/help handlers
    for handler in start_handlers:
        application.add_handler(handler)

    # Register search handler
    application.add_handler(MessageHandler(filters.Regex("^🔍 Search Movies$"), search_movies))
    application.add_handler(MessageHandler(filters.Regex("^📂 Browse Categories$"), browse_categories))

    # Register callback handler (catches all callback queries)
    application.add_handler(callback_query_handler)

    # Register search text handler (for when user types search query)
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & ~filters.Regex("^(➕|🗑️|📊|👥|📢|❓|❌|🔍|📂|🙏)"),
        handle_search_query
    ))

    # Channel member handler
    application.add_handler(ChatMemberHandler(welcome_new_member, ChatMemberHandler.CHAT_MEMBER))

    # Global cancel
    application.add_handler(CommandHandler("cancel", global_cancel_handler))

    # Error handler
    application.add_error_handler(error_handler)

    logger.info(f"✅ Bot application built with all handlers")
    return application


def run_bot_in_thread():
    """Run bot in a separate thread with its own event loop"""
    application = build_application()
    if not application:
        logger.error("❌ Failed to build bot application")
        return

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def start_bot():
        """Initialize and start the bot"""
        await application.initialize()
        await application.start()

        # Notify owner
        try:
            await application.bot.send_message(
                chat_id=OWNER_ID,
                text="🤖 MovieZone Bot started successfully!\n\n"
                     "📡 Integrated Server Mode"
            )
        except Exception as e:
            logger.warning(f"Could not notify owner: {e}")

        logger.info(f"🚀 Bot @{BOT_USERNAME} is polling...")

        # Start polling (this runs until stopped)
        await application.updater.start_polling(drop_pending_updates=True)

        # Keep running
        try:
            while True:
                await asyncio.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            await application.updater.stop()
            await application.stop()
            await application.shutdown()

    try:
        loop.run_until_complete(start_bot())
    except Exception as e:
        logger.error(f"Bot error: {e}")
    finally:
        loop.close()