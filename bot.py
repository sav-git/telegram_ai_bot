from openai import OpenAI
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import logging
import db

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global OpenAI client
client = None

def chat_with_gpt(prompt, user_id):
    """Function to interact with OpenAI API"""
    try:
        user_history = db.get_user_history(user_id)
        messages = user_history + [{"role": "user", "content": prompt}]
    except Exception as e:
        logger.error(f"Error retrieving user history: {e}")
        messages = [{"role": "user", "content": prompt}]
    
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3-8b-instruct",
            messages=messages,
        )
        # Save messages to database
        db.save_user_message(user_id, "user", prompt)
        db.save_user_message(user_id, "assistant", response.choices[0].message.content)
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        return "Sorry, I'm having trouble processing your request right now."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages"""
    user_message = update.message.text
    user_id = update.effective_user.id
    
    # Send typing action
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        response = chat_with_gpt(user_message, user_id)
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        await update.message.reply_text("Sorry, an error occurred. Please try again.")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command"""
    await update.message.reply_text("🤖 Hello! I'm your AI assistant bot.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command"""
    await update.message.reply_text("Send me any message and I'll respond!")

def main():
    """Main function to run the bot"""
    load_dotenv()
    
    # Initialize database
    db.init_db()
    
    # Get API keys
    openrouter_api_key = os.getenv("OpenRouter_API_KEY")
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not all([openrouter_api_key, telegram_bot_token]):
        logger.error("Missing environment variables")
        return
    
    # Initialize OpenAI client
    global client
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_api_key
    )
    
    # Create the Application
    application = Application.builder().token(telegram_bot_token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
