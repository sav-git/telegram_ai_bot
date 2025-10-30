from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command"""
    await update.message.reply_text("🤖 Hello! I'm your AI assistant bot.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command"""
    await update.message.reply_text("Send me any message and I'll respond!")

def main():
    """Main function to run the bot"""
    # Get bot token from environment
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not telegram_bot_token:
        logger.error("TELEGRAM_BOT_TOKEN not found")
        return
    
    # Create the Application
    application = Application.builder().token(telegram_bot_token).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Start the bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
